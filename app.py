import json

import requests
from flask import Flask, render_template, request

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
    data_dict = {"title": meal_str, "category": meal_category, "area": meal_str_area, "instructions": meal_instructions,
                 "ingredients": json.dumps(meal_ingredients), "img_url": meal_img_url}
    json_data = json.dumps(data_dict)

    html_start = (f"<h2>{meal_str}</h2>"
                  f"<img src='{meal_img_url}' alt='{meal_str}'>"
                  f"<p><strong>Category: </strong>{meal_category}</p>"
                  f"<p><strong>Area: </strong>{meal_str_area}</p>")
    html_end = (f"<p><strong>Instructions: </strong>{meal_instructions}</p>"
                "<button id='saved_meals' class='button save' hx-post='/add_meal' hx-vals=\'"
                f'{json_data}'
                "\' hx-target='#meal_confirm' hx-trigger='click'>Add To Saved Meals</button>"
                "<div id='meal_confirm'></div>")
    html_ingredients = get_ingredient_html(meal_ingredients)

    return html_start + html_ingredients + html_end

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
    data_dict = {"title": drink_str, "category": drink_category, "instructions": drink_instructions,
                 "ingredients": json.dumps(drink_ingredients), "img_url": drink_img_url}
    json_data = json.dumps(data_dict)

    html_start = (f"<h2>{drink_str}</h2><img src={drink_img_url} alt={drink_str}>"
                  f"<p><strong>Category: </strong>{drink_category}</p>")
    html_end = (f"<p><strong>Instructions: </strong>{drink_instructions}</p>"
                '<button class="button save" hx-post="/add_drink" hx-vals=\''
                f'{json_data}'
                '\' hx-target="#drink_confirm" hx-trigger="click">Add To Saved Drinks</button>'
                "<div id='drink_confirm'></div>")
    html_ingredients = get_ingredient_html(drink_ingredients)

    return html_start + html_ingredients + html_end

def make_ingredient_list(type_dict, start, end):
    ingredient_list = []
    end += 1  # This makes sure that we get the last ingredient too!!!

    for i in range(start, end):
        attribute_name = f'strIngredient{i}'
        ingredient = type_dict.get(attribute_name)

        if ingredient is not None and ingredient != "":
            ingredient_list.append(ingredient)

    return ingredient_list

def get_ingredient_html(ingredient_list):
    html_ingredients = "<p><strong>Ingredients: </strong>"

    for i, ingredient in enumerate(ingredient_list):
        if i == len(ingredient_list) - 1:
            html_ingredients += ingredient
        else:
            html_ingredients += ingredient + ", "
    html_ingredients += "</p>"

    return html_ingredients

@app.post('/add_drink')
def add_drink():
    title = request.form.get('title')
    img_url = request.form.get("img_url")
    category = request.form.get("category")
    instructions = request.form.get("instructions")
    # This is an array so we had to convert this to json before we sent it so we re-load it here!
    ingredients = json.loads(request.form.get("ingredients"))

    return "Added the drink successfully!"

@app.post('/add_meal')
def add_meal():
    title = request.form.get("title")
    img_url = request.form.get("img_url")
    category = request.form.get("category")
    instructions = request.form.get("instructions")
    area = request.form.get("area")
    # This is an array so we had to convert this to json before we sent it so we re-load it here!
    ingredients = json.loads(request.form.get("ingredients"))

    return "Added the meal successfully!"

@app.get('/write')
def write_recipe():
    return render_template("write_recipe.html")

if __name__ == '__main__':
    app.run(port=5000)

