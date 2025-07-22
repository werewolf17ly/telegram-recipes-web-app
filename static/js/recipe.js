let tg = window.Telegram.WebApp;
tg.expand();
tg.MainButton.text = "Добавить в корзину";
tg.MainButton.show();

const recipeId = window.location.pathname.split('/').pop();
let currentRecipe = null;

document.addEventListener('DOMContentLoaded', function() {
    loadRecipe();
    loadNutrition();
    
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

async function loadNutrition() {
    try {
        const response = await fetch(`/api/recipes/${recipeId}/nutrition`);
        const nutritionData = await response.json();
        
        if (nutritionData.error) {
            showNutritionError();
        } else {
            displayNutrition(nutritionData);
        }
    } catch (error) {
        console.error('Error loading nutrition:', error);
        showNutritionError();
    }
}

function displayNutrition(nutrition) {
    // Скрываем индикатор загрузки
    document.getElementById('nutrition-loading').style.display = 'none';
    
    // Показываем контент с данными
    document.getElementById('nutrition-content').style.display = 'block';
    
    // Заполняем основные показатели
    document.getElementById('calories-value').textContent = Math.round(nutrition.calories || 0);
    document.getElementById('proteins-value').textContent = Math.round(nutrition.proteins || 0);
    document.getElementById('fats-value').textContent = Math.round(nutrition.fats || 0);
    document.getElementById('carbs-value').textContent = Math.round(nutrition.carbohydrates || 0);
    
    // Заполняем дополнительные показатели
    document.getElementById('fiber-value').textContent = `${Math.round(nutrition.fiber || 0)} г`;
    document.getElementById('sugar-value').textContent = `${Math.round(nutrition.sugar || 0)} г`;
    document.getElementById('sodium-value').textContent = `${Math.round(nutrition.sodium || 0)} мг`;
    document.getElementById('servings-value').textContent = nutrition.servings || 1;
}

function showNutritionError() {
    // Скрываем индикатор загрузки
    document.getElementById('nutrition-loading').style.display = 'none';
    
    // Показываем сообщение об ошибке
    document.getElementById('nutrition-error').style.display = 'block';
}
