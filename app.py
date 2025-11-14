from flask import Flask, render_template
import requests
import json

from model import Drinks, Meals
from model.base import db

app = Flask(__name__, static_url_path='/static', static_folder='static')

with db:
    db.create_tables([Drinks, Meals])


@app.before_request
def _db_connect():
    db.connect()


# This hook ensures that the connection is closed when we've finished
# processing the request.
@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()

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
    html_start = (f"<h2>{meal_str}</h2>"
                  f"<img src='{meal_img_url}' alt='{meal_str}'>"
                  f"<p><strong>Category: </strong>{meal_category}</p>"
                  f"<p><strong>Area: </strong>{meal_str_area}</p>")
    html_end = (f"<p><strong>Instructions: </strong>{meal_instructions}</p>"
                "<button id='saved_meals' class='button save' hx-post='/add_meal' hx-trigger='click'>Add To Saved Meals</button>"
                "<div id='meal_confirm'></div>")
    html_ingredients = get_ingredient_html(meal, 1, 20)

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
    html_start = (f"<h2>{drink_str}</h2><img src={drink_img_url} alt={drink_str}>"
                  f"<p><strong>Category: </strong>{drink_category}</p>")
    html_end = (f"<p><strong>Instructions: </strong>{drink_instructions}</p>"
                "<button class='button save' hx-post='/add_drink' hx-target='drink_confirm' hx-trigger='click'>Add To Saved Drinks</button>"
                "<div id='drink_confirm'></div>>")
    html_ingredients = get_ingredient_html(drink, 1, 4)

    return html_start + html_ingredients + html_end

def get_ingredient_html(type_dict, start, end):
    html_ingredients = "<p><strong>Ingredients: </strong>"
    ingredient_list = []
    end += 1 # This makes sure that we get the last ingredient too!!!

    for i in range(start, end):
        attribute_name = f'strIngredient{i}'
        ingredient = type_dict.get(attribute_name)

        if ingredient is not None and ingredient != "":
            ingredient_list.append(ingredient)

    for i, ingredient in enumerate(ingredient_list):
        if i == len(ingredient_list) - 1:
            html_ingredients += ingredient
        else:
            html_ingredients += ingredient + ", "
    html_ingredients += "</p>"

    return html_ingredients

@app.post('/add_drink')
def add_drink():
    pass

@app.post('/add_meal')
def add_meal():
    pass

@app.get('/write')
def write_recipe():
    return render_template("write_recipe.html")

if __name__ == '__main__':
    app.run(port=5000)

