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
    try:
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
    except requests.exceptions.ConnectionError:
        return "<p>Cannot get data from the meals API, check your internet connection!<p>"


@app.get('/drinks')
def drinks():
    try:
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
    except requests.exceptions.ConnectionError:
        return "<p>Cannot get data from the drinks API, check your internet connection!<p>"



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
        temp_dir = "./tmp"

        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        fd, temp_name = tempfile.mkstemp(dir=temp_dir)
        os.close(fd)

        if not os.path.exists("drinks.json") or (os.path.exists("drinks.json") and os.path.getsize("drinks.json") == 0):
            with open(temp_name, "w") as drink_temp:
                drink_data["id"] = 0
                drink_data_list = [drink_data]
                drink_data_json = json.dumps(drink_data_list)
                drink_temp.write(drink_data_json)
                drink_temp.flush()

            temp_path = os.path.join(temp_dir, drink_temp.name)

            try:
                os.replace(temp_path, "drinks.json")
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
        else:
            with open("drinks.json", "r") as drink_file, open(temp_name, "w") as drink_temp:
                drink_data_list = json.loads(drink_file.read())
                drink_data["id"] = get_next_id(drink_data_list)
                drink_data_list.append(drink_data)
                drink_data_json = json.dumps(drink_data_list, indent=2)
                drink_temp.write(drink_data_json)
                drink_temp.flush()

            temp_path = os.path.join(temp_dir, drink_temp.name)

            try:
                os.replace(temp_path, drink_file.name)
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

        return f'Added {drink_data.get("title")} to your drinks successfully!'
    else:
        return f'Failed to add to your drinks'


def get_next_id(data_list):
    if data_list:
        last_index = len(data_list) - 1
        next_id = data_list[last_index].get("id") + 1
        return next_id
    else:
        return 0

@app.post('/add_meal')
def add_meal():
    meal_data = {}

    # This is a workaround for not being able to send all the data across,
    # since it wouldn't send if it got too large sometimes!
    with open("internals/meal.json", "r") as f:
        meal_data = json.loads(f.read())

    if meal_data is not None:
        temp_dir = "./tmp"

        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        fd, temp_name = tempfile.mkstemp(dir=temp_dir)
        os.close(fd)

        if not os.path.exists("meals.json") or (os.path.exists("meals.json") and os.path.getsize("meals.json") == 0):
            with open(temp_name, "w") as meal_temp:
                meal_data_list = [meal_data]
                meal_data["id"] = 0
                meal_data_json = json.dumps(meal_data_list)
                meal_temp.write(meal_data_json)
                meal_temp.flush()

            temp_path = os.path.join(temp_dir, meal_temp.name)

            try:
                os.replace(temp_path, "meals.json")
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
        else:
            with open("meals.json", "r") as meal_file, open(temp_name, "w") as meal_temp:
                meal_data_list = json.loads(meal_file.read())
                meal_data["id"] = get_next_id(meal_data_list)
                meal_data_list.append(meal_data)
                meal_data_json = json.dumps(meal_data_list, indent=2)
                meal_temp.write(meal_data_json)
                meal_temp.flush()

            temp_path = os.path.join(temp_dir, meal_temp.name)

            try:
                os.replace(temp_path, meal_file.name)
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

        return f'Added {meal_data.get("title")} to your meals successfully!'
    else:
        return f'Failed to add to your meals'


@app.delete('/delete_meal/<idx>')
def delete_meal(idx):
    temp_dir = "./tmp"
    meal_id = int(idx)

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    fd, temp_name = tempfile.mkstemp(dir=temp_dir)
    os.close(fd)

    with open("meals.json", "r") as meals_file, open(temp_name, "w") as meal_tmp:
        meals_dict = json.loads(meals_file.read()) # Here we load in the list of meals that the user has saved!

        for i, meal in enumerate(meals_dict):
            if meal.get("id") == meal_id:
                del meals_dict[i]
                break

        meal_json = json.dumps(meals_dict, indent=2) # Convert the new content to json!
        meal_tmp.write(meal_json)
        meal_tmp.flush()

    temp_path = os.path.join(temp_dir, meal_tmp.name)

    try:
        os.replace(temp_path, meals_file.name)
        if not meals_dict:
            return "<p>You haven't saved any meals yet!</p>" # A workaround so that the last meal does not get replaced by a blank box!
        else:
            return "" # Effectively removes the content that was displayed for the entry!
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path) # Clean up the temporary file!


@app.delete('/delete_drink/<idx>')
def delete_drink(idx):
    temp_dir = "./tmp"
    drink_id = int(idx)

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    fd, temp_name = tempfile.mkstemp(dir=temp_dir)
    os.close(fd)

    with open("drinks.json", "r") as drinks_file, open(temp_name, "w") as drink_tmp:
        drinks_dict = json.loads(drinks_file.read()) # Here we load in the list of drinks that the user has saved!

        for i, drink in enumerate(drinks_dict):
            if drink.get("id") == drink_id:
                del drinks_dict[i]
                break

        drinks_json = json.dumps(drinks_dict, indent=2) # Convert the new content to json!
        drink_tmp.write(drinks_json)
        drink_tmp.flush()

    temp_path = os.path.join(temp_dir, drink_tmp.name)

    try:
        os.replace(temp_path, drinks_file.name)
        if not drinks_dict:
            return "<p>You haven't saved any drinks yet!</p>" # A workaround so the last entry does not get replaced by a blank box!
        else:
            return "" # Effectively removes the content that was displayed for the entry!
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path) # Clean up the temporary file!


@app.get('/my_drinks')
def my_drinks():
    drinks_list = []

    with open("drinks.json", "r") as drinks_data:
        if drinks_data:
            drinks_list = json.loads(drinks_data.read())

    my_drinks_template = env.get_template("my_drinks.html")

    return my_drinks_template.render(drinks=drinks_list)

@app.post('/drink_search')
def drink_search():
    drinks_list = []
    search = request.form.get("drink_search")

    with open("drinks.json", "r") as drinks_data:
        if drinks_data:
            drinks_list = json.loads(drinks_data.read())

    if not drinks_list:
        return "<p>You haven't saved any drinks yet!</p>"

    if search:
        filtered_drinks = filter(lambda drink: search.lower() in drink.get('title').lower(), drinks_list)
        drinks_list = list(filtered_drinks)

    drink_search_template = env.get_template("saved_drinks.html")

    if not drinks_list:
        return "<p>No drinks match the search!</p>"
    else:
        return drink_search_template.render(drinks=drinks_list)

@app.get('/my_meals')
def my_meals():    
    meals_list = []

    with open("meals.json", "r") as meals_data:
        if meals_data:
            meals_list = json.loads(meals_data.read())

    my_meals_template = env.get_template("my_meals.html")

    return my_meals_template.render(meals=meals_list)

if __name__ == '__main__':
    if os.uname().nodename == 'csci331vm.cs.montana.edu':
        app.run(host='csci331vm.cs.montana.edu', port=3001)
    else:
        app.run(port=5000)
