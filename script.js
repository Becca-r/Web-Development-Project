
import { createServer } from 'node:http';


const server = createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.write('Hello World!\n');
  res.end('Hello Becca!\n');
});


server.listen(3016, '127.0.0.1', () => {
  console.log('Listening on 127.0.0.1:3016');
});


const recipeDiv = document.getElementById('recipe');


    document.getElementById('browse').addEventListener('click', async () => {
      const res = await fetch('https://www.themealdb.com/api/json/v1/1/random.php');
      const data = await res.json();
      const meal = data.meals[0];
      recipeDiv.innerHTML = `
        <h2>${meal.strMeal}</h2>
        <img src="${meal.strMealThumb}" alt="${meal.strMeal}">
        <p><strong>Category:</strong> ${meal.strCategory}</p>
        <p><strong>Area:</strong> ${meal.strArea}</p>
        <p><strong>Ingredients:</strong> ${[meal.strIngredients1, meal.strIngredients2, meal.strIngredients3, meal.strIngredients4].filter(Boolean).join(', ')}</p>
        <p><strong>Instructions:</strong> ${meal.strInstructions}...</p>
`;
    });

    document.getElementById('drinks').addEventListener('click', async () => {
      const res = await fetch('https://www.thecocktaildb.com/api/json/v1/1/random.php');
      const data = await res.json();
      const drink = data.drinks[0];
      recipeDiv.innerHTML = `
        <h2>${drink.strDrink}</h2>
        <img src="${drink.strDrinkThumb}" alt="${drink.strDrink}">
        <p><strong>Category:</strong> ${drink.strCategory}</p>
        <p><strong>Ingredients:</strong> ${
          [drink.strIngredient1, drink.strIngredient2, drink.strIngredient3, drink.strIngredient4]
            .filter(Boolean).join(', ')}</p>
        <p><strong>Instructions:</strong> ${drink.strInstructions}</p>
      `;
    });


    document.getElementById('write').addEventListener('click', () => {
      recipeDiv.innerHTML = `
        <h2>Write Your Own Recipe </h2>
        <input type="text" id="recipeTitle" placeholder="Recipe title..." style="width:100%;padding:8px;border-radius:8px;border:1px solid #ccc;">
        <textarea id="customRecipe" placeholder="Write your ingredients and steps here..."></textarea>
        <button class="button save" id="saveRecipe">Save Recipe</button>
      `;

      document.getElementById('saveRecipe').addEventListener('click', () => {
        const title = document.getElementById('recipeTitle').value.trim();
        const text = document.getElementById('customRecipe').value.trim();

        let saved = JSON.parse(localStorage.getItem('myRecipes') || '[]');
        saved.push({ title, text, date: new Date().toLocaleString() });
        localStorage.setItem('myRecipes', JSON.stringify(saved));
        alert(' Your recipe has been saved!');
      });
    });


    document.getElementById('myRecipes').addEventListener('click', () => {
      const saved = JSON.parse(localStorage.getItem('myRecipes') || '[]');

      if (saved.length === 0) {
        recipeDiv.innerHTML = `<p>You haven't saved any recipes yet!</p>`;
        return;
      }

      recipeDiv.innerHTML = '<h2> My Saved Recipes</h2>';
      saved.forEach((r, i) => {
        const div = document.createElement('div');
        div.classList.add('recipe-card');
        div.innerHTML = `
          <h3>${r.title}</h3>
          <p><em>Saved on: ${r.date}</em></p>
          <p>${r.text.replace(/\n/g, '<br>')}</p>
          <button class="button" style="background-color:red" data-index="${i}"> Delete</button>
        `;
        recipeDiv.appendChild(div);
      });

 
      document.querySelectorAll('[data-index]').forEach(btn => {
        btn.addEventListener('click', e => {
          const index = e.target.getAttribute('data-index');
          const updated = saved.filter((_, i) => i != index);
          localStorage.setItem('myRecipes', JSON.stringify(updated));
          e.target.parentElement.remove();
        });
      });
    });