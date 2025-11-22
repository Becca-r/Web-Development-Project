import os
import json
import tempfile

import requests
from jinja2 import Environment, FileSystemLoader
from flask import Flask, render_template, request

env = Environment(loader=FileSystemLoader('./templates'))


app = Flask(__name__, static_url_path='/static', static_folder='static')


@app.route('/')
def index():
    return render_template("Home.html")


@app.get('/browse')
def browse_recipes():
    res = requests.get('https://www.themealdb.com/api/json/v1/1/random.php')
    data = json.loads(res.text)
    meal = data.get('meals')[0]
    meal_str = meal.get('strMeal')
    meal_img_url = meal.get('strMealThumb')
    meal_category = meal.get('strCategory')
    meal_str_area = meal.get('strArea')
    meal_instructions = meal.get('strInstructions')
    meal_ingredients = make_ingredient_list(meal, 1, 20)
    meal_data = {"title": meal_str, "category": meal_category, "area": meal_str_area, "instructions": meal_instructions, "img_url": meal_img_url, "ingredients": meal_ingredients}
    json_meal_data = json.dumps(meal_data)
    file_path = "internals/meal.json"
    directory = os.path.dirname(file_path)

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(file_path, "w") as meal_file:
        meal_file.write(json_meal_data)

    browse_recipes_template = env.get_template("browse_recipe.html")

    return browse_recipes_template.render(meal_data)


@app.get('/drinks')
def drinks():
    res = requests.get('https://www.thecocktaildb.com/api/json/v1/1/random.php')
    data = json.loads(res.text)
    drink = data.get('drinks')[0]
    drink_str = drink.get('strDrink')
    drink_img_url = drink.get('strDrinkThumb')
    drink_category = drink.get('strCategory')
    drink_instructions = drink.get('strInstructions')
    drink_ingredients = make_ingredient_list(drink, 1, 4)
    drink_data = {"title": drink_str, "category": drink_category, "instructions": drink_instructions,
                 "ingredients": drink_ingredients, "img_url": drink_img_url}
    json_drink_data = json.dumps(drink_data)
    file_path = "internals/drink.json"
    directory = os.path.dirname(file_path)

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(file_path, "w") as drink_file:
        drink_file.write(json_drink_data)

    drinks_template = env.get_template("drinks.html")

    return drinks_template.render(drink_data)


def make_ingredient_list(type_dict, start, end):
    ingredient_list = []
    end += 1  # This makes sure that we get the last ingredient too!!!

    for i in range(start, end):
        attribute_name = f'strIngredient{i}'
        ingredient = type_dict.get(attribute_name)


        if ingredient is not None and ingredient != "":
            ingredient_list.append(ingredient)

    return ingredient_list

@app.post('/add_drink')
def add_drink():
    drink_data = {}

    # This is a workaround for not being able to send all the data across,
    # since it wouldn't send if it got too large sometimes!
    with open("internals/drink.json", "r") as f:
        drink_data = json.loads(f.read())

    if drink_data is not None:
        # TODO: Write the json to the file here please for drinks!
        drinks = {}
        if os.path.exists("drinks.json"):
            with open ("drinks.json", "r") as f:
                try:
                    drinks = json.load(f)
                except json.JSONDecodeError:
                    drinks = {}
        drinks[drink_data.get("title")] = {"category": drink_data.get("category"),
                                           "instructions": drink_data.get("instructions"),
                                           "ingredients": drink_data.get("ingredients"),
                                           "img_url": drink_data.get("img_url")}

        with open("drinks.json", "w") as f:
           saved_drinks = json.loads(f.read())
           saved_drinks.update(drinks)

        return f"Added {drink_data.get("title")} to your drinks successfully!"
    else:
        return f"Failed to add to your drinks"


@app.post('/add_meal')
def add_meal():
    meal_data = {}

    # This is a workaround for not being able to send all the data across,
    # since it wouldn't send if it got too large sometimes!
    with open("internals/meal.json", "r") as f:
        meal_data = json.loads(f.read())

    if meal_data is not None:
        # TODO: Write the json to the file here please for meals!
        meals = {}
        if os.path.exists("meals.json"):
            with open ("meals.json", "r") as f:
                try:
                    meals = json.load(f)
                except json.JSONDecodeError:
                    meals = {}
        meals[meal_data.get("title")] = {"category": meal_data.get("category"), "area": meal_data.get("area"),
                                  "instructions": meal_data.get("instructions"),
                                  "ingredients": meal_data.get("ingredients"), "img_url": meal_data.get("img_url")}

        with open("meals.json", "w") as f:
            saved_meals = json.loads(f.read())
            saved_meals.update(meals)
        return f"Added {meal_data.get("title")} to your meals successfully!"
    else:
        return f"Failed to add to your meals"


@app.delete('/delete_meal/<idx>')
def delete_meal(idx):

    with open("meals.json", "r") as meals_file, tempfile.NamedTemporaryFile(delete_on_close=False) as meal_tmp:
        meals = json.loads(meals_file.read()) # Here we load in the list of meals that the user has saved!
        meals.pop(idx)
        meal_json = json.dumps(meals) # Convert the new content to json!
        meal_tmp.write(meal_json)

    # In case of a power outage we first wrote to a temporary file,
    # so now we can replace the original content with the content from the temporary file!
    try:
        os.replace(meal_tmp.name, meals_file.name)
        return "", 204  # Effectively removes the content that was displayed for the entry and returns 204 (No Content)!
    finally:
        os.remove(meal_tmp.name) # The finally block makes sure that the temporary file is cleaned up!


@app.delete('/delete_drink/<idx>')
def delete_drink(idx):

    with open("drinks.json", "r") as drinks_file, tempfile.NamedTemporaryFile(delete_on_close=False) as drink_tmp:
        drinks_dict = json.loads(drinks_file.read()) # Here we load in the list of drinks that the user has saved!
        drinks_dict.pop(idx)
        drinks_json = json.dumps(drinks) # Convert the new content to json!
        drink_tmp.write(drinks_json)

    # In case of a power outage we first wrote to a temporary file,
    # so now we can replace the original content with the content from the temporary file!
    try:
        os.replace(drink_tmp.name, drinks_file.name)
        return "", 204 # Effectively removes the content that was displayed for the entry and returns 204 (No Content)!
    finally:
        os.remove(drink_tmp.name) # The finally block makes sure that the temporary file is cleaned up!


@app.get('/write')
def write_recipe():
    return render_template("write_recipe.html")


@app.get('/my_recipes')
def my_recipes():
    return "<p>You haven't saved any recipes yet!</p>"

if __name__ == '__main__':
    app.run(port=5000)
