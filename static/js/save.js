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

document.getElementById('myRecipes').addEventListener('click', () => {
  const saved = JSON.parse(localStorage.getItem('myRecipes') || '[]');
  const recipeDiv = document.getElementById('recipe');

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
      const updated = saved.filter((_, i) => i !== index);
      localStorage.setItem('myRecipes', JSON.stringify(updated));
      e.target.parentElement.remove();
    });
  });
});