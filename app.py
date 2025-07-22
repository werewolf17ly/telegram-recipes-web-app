from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

# Данные о рецептах
RECIPES = [
    {
        "id": 1,
        "name": "Паста Карбонара",
        "image": "https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=400",
        "description": "Классическая итальянская паста с беконом и сыром",
        "ingredients": [
            {"name": "спагетти", "amount": "400г"},
            {"name": "бекон", "amount": "200г"},
            {"name": "яйца", "amount": "3 шт"},
            {"name": "пармезан", "amount": "100г"},
            {"name": "черный перец", "amount": "по вкусу"}
        ],
        "instructions": "1. Отварите спагетти до аль денте\n2. Обжарьте бекон до хрустящей корочки\n3. Взбейте яйца с сыром\n4. Смешайте все ингредиенты",
        "alternatives": {
            "бекон": ["ветчина", "копченая грудка", "соевое мясо"],
            "пармезан": ["пекорино", "грана падано", "сыр чеддер"]
        }
    },
    {
        "id": 2,
        "name": "Цезарь салат",
        "image": "https://images.unsplash.com/photo-1551248429-40975aa4de74?w=400",
        "description": "Классический салат с курицей и соусом цезарь",
        "ingredients": [
            {"name": "курица", "amount": "300г"},
            {"name": "салат ромэн", "amount": "1 пучок"},
            {"name": "пармезан", "amount": "50г"},
            {"name": "сухари", "amount": "100г"},
            {"name": "соус цезарь", "amount": "3 ст.л."}
        ],
        "instructions": "1. Обжарьте курицу до готовности\n2. Нарежьте салат\n3. Добавьте курицу и сухари\n4. Полейте соусом и посыпьте сыром",
        "alternatives": {
            "курица": ["индейка", "тунец", "тофу"],
            "салат ромэн": ["айсберг", "шпинат", "латук"]
        }
    },
    {
        "id": 3,
        "name": "Борщ",
        "image": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=400",
        "description": "Традиционный русский суп со свеклой",
        "ingredients": [
            {"name": "говядина", "amount": "500г"},
            {"name": "свекла", "amount": "2 шт"},
            {"name": "капуста", "amount": "300г"},
            {"name": "картофель", "amount": "3 шт"},
            {"name": "морковь", "amount": "2 шт"}
        ],
        "instructions": "1. Отварите бульон из говядины\n2. Добавьте нарезанные овощи\n3. Варите до готовности\n4. Подавайте со сметаной",
        "alternatives": {
            "говядина": ["свинина", "курица", "грибы"],
            "свекла": ["морковь", "редька", "сладкий картофель"]
        }
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/recipes')
def get_recipes():
    return jsonify(RECIPES)

@app.route('/api/recipes/<int:recipe_id>')
def get_recipe(recipe_id):
    recipe = next((r for r in RECIPES if r['id'] == recipe_id), None)
    if recipe:
        return jsonify(recipe)
    return jsonify({'error': 'Recipe not found'}), 404

@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    return render_template('recipe.html', recipe_id=recipe_id)

@app.route('/cart/<int:recipe_id>')
def cart(recipe_id):
    return render_template('cart.html', recipe_id=recipe_id)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
