let tg = window.Telegram.WebApp;
tg.expand();
tg.MainButton.text = "Подтвердить выбор";
tg.MainButton.show();

const recipeId = window.location.pathname.split('/').pop();
let selectedAlternatives = {};
let recipeData = null;

document.addEventListener('DOMContentLoaded', function() {
    loadCartData();
    
    tg.MainButton.onClick(() => {
        confirmSelection();
    });
});

async function loadCartData() {
    try {
        const response = await fetch(`/api/recipes/${recipeId}`);
        recipeData = await response.json();
        displayCart(recipeData);
    } catch (error) {
        console.error('Error loading cart data:', error);
    }
}

function displayCart(recipe) {
    const container = document.getElementById('cart-content');
    container.innerHTML = '';
    
    const title = document.createElement('h2');
    title.textContent = `Рецепт: ${recipe.name}`;
    container.appendChild(title);
    
    recipe.ingredients.forEach(ingredient => {
        const alternatives = recipe.alternatives[ingredient.name] || [];
        if (alternatives.length > 0) {
            const section = document.createElement('div');
            section.className = 'alternative-item';
            
            section.innerHTML = `
                <h4>${ingredient.name} (${ingredient.amount})</h4>
                <div class="alternative-options">
                    <div class="alternative-option selected" data-original="${ingredient.name}">
                        ${ingredient.name} (оригинал)
                    </div>
                    ${alternatives.map(alt => `
                        <div class="alternative-option" data-original="${ingredient.name}" data-alternative="${alt}">
                            ${alt}
                        </div>
                    `).join('')}
                </div>
            `;
            
            container.appendChild(section);
        }
    });
    
    // Add click handlers for alternatives
    document.querySelectorAll('.alternative-option').forEach(option => {
        option.addEventListener('click', function() {
            const original = this.dataset.original;
            const parent = this.parentElement;
            
            // Remove selected from siblings
            parent.querySelectorAll('.alternative-option').forEach(opt => {
                opt.classList.remove('selected');
            });
            
            // Add selected to clicked option
            this.classList.add('selected');
            
            // Store selection
            selectedAlternatives[original] = this.dataset.alternative || original;
        });
    });
}

function confirmSelection() {
    const selections = Object.entries(selectedAlternatives).map(([original, selected]) => {
        return `${original} → ${selected}`;
    }).join(', ');
    
    tg.sendData(`Выбранные аналоги: ${selections}`);
    tg.close();
}
