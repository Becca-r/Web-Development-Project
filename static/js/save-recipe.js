document.getElementById("recipe").addEventListener('htmx:afterSwap', (event) => {
  const saveRecipeButton = document.getElementById('saveRecipe');

  if (saveRecipeButton !== null) {
    document.getElementById('saveRecipe').addEventListener('click', saveRecipeOnClick);
  }
});

function saveRecipeOnClick() {
  const title = document.getElementById('recipeTitle').value.trim();
  const text = document.getElementById('customRecipe').value.trim();
  const recipe = { title, text, date: new Date().toLocaleString() };

  let saved = JSON.parse(localStorage.getItem('myRecipes') || '[]');
  saved.push({ title, text, date: new Date().toLocaleString() });
  localStorage.setItem('myRecipes', JSON.stringify(saved));
  alert(' Your recipe has been saved!');
}