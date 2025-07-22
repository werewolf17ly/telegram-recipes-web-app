let tg = window.Telegram.WebApp;
tg.expand();
tg.MainButton.text = "Добавить в корзину";
tg.MainButton.show();

const recipeId = window.location.pathname.split('/').pop();
let currentRecipe = null;

document.addEventListener('DOMContentLoaded', function() {
    loadRecipe();
    
    tg.MainButton.onClick(() => {
        if (currentRecipe) {
            window.location.href = `/cart/${recipeId}`;
        }
    });
});

async function loadRecipe() {
    try {
        const response = await fetch(`/api/recipes/${recipeId}`);
        currentRecipe = await response.json();
        displayRecipe(currentRecipe);
    } catch (error) {
        console.error('Error loading recipe:', error);
    }
}

function displayRecipe(recipe) {
    document.getElementById('recipe-image').src = recipe.image;
    document.getElementById('recipe-name').textContent = recipe.name;
    document.getElementById('recipe-description').textContent = recipe.description;
    
    const ingredientsList = document.getElementById('ingredients-list');
    ingredientsList.innerHTML = '';
    recipe.ingredients.forEach(ingredient => {
        const li = document.createElement('li');
        li.textContent = `${ingredient.name} - ${ingredient.amount}`;
        ingredientsList.appendChild(li);
    });
    
    document.getElementById('recipe-instructions').textContent = recipe.instructions;
}
