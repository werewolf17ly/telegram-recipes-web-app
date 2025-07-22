let tg = window.Telegram.WebApp;
tg.expand();

document.addEventListener('DOMContentLoaded', function() {
    loadRecipes();
});

async function loadRecipes() {
    try {
        const response = await fetch('/api/recipes');
        const recipes = await response.json();
        displayRecipes(recipes);
    } catch (error) {
        console.error('Error loading recipes:', error);
    }
}

function displayRecipes(recipes) {
    const container = document.getElementById('recipes-list');
    container.innerHTML = '';
    
    recipes.forEach(recipe => {
        const card = createRecipeCard(recipe);
        container.appendChild(card);
    });
}

function createRecipeCard(recipe) {
    const card = document.createElement('div');
    card.className = 'recipe-card';
    card.onclick = () => openRecipe(recipe.id);
    
    card.innerHTML = `
        <img src="${recipe.image}" alt="${recipe.name}">
        <div class="recipe-card-content">
            <h3>${recipe.name}</h3>
            <p>${recipe.description}</p>
        </div>
    `;
    
    return card;
}

function openRecipe(recipeId) {
    window.location.href = `/recipe/${recipeId}`;
}
