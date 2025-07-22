from flask import Flask, render_template, jsonify, request
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Конфигурация OpenRouter API
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

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

def calculate_nutrition(recipe_data):
    """Рассчитывает питательную ценность рецепта через OpenRouter API"""
    if not OPENROUTER_API_KEY:
        return {"error": "OpenRouter API key not configured"}
    
    # Формируем список ингредиентов для анализа
    ingredients_text = "\n".join([f"- {ing['name']}: {ing['amount']}" for ing in recipe_data['ingredients']])
    
    system_prompt = """Ты эксперт по питанию. Рассчитай точную питательную ценность блюда на основе списка ингредиентов.

Верни результат СТРОГО в следующем JSON формате:
{
    "calories": число_калорий_на_порцию,
    "proteins": граммы_белков,
    "fats": граммы_жиров,
    "carbohydrates": граммы_углеводов,
    "fiber": граммы_клетчатки,
    "sugar": граммы_сахара,
    "sodium": миллиграммы_натрия,
    "servings": количество_порций
}

Используй точные данные о питательной ценности продуктов. Учитывай потери при термической обработке."""

    user_prompt = f"""Рецепт: {recipe_data['name']}
Описание: {recipe_data['description']}

Ингредиенты:
{ingredients_text}

Способ приготовления:
{recipe_data['instructions']}

Рассчитай питательную ценность этого блюда."""

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "openai/gpt-4o",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.1,
            "max_tokens": 500
        }
        
        response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        ai_response = result['choices'][0]['message']['content'].strip()
        
        # Парсим JSON ответ от AI
        try:
            nutrition_data = json.loads(ai_response)
            return nutrition_data
        except json.JSONDecodeError:
            # Если AI вернул не JSON, пытаемся извлечь JSON из текста
            import re
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                nutrition_data = json.loads(json_match.group())
                return nutrition_data
            else:
                return {"error": "Failed to parse AI response"}
                
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}
    except Exception as e:
        return {"error": f"Calculation failed: {str(e)}"}

@app.route('/api/recipes/<int:recipe_id>/nutrition')
def get_recipe_nutrition(recipe_id):
    """API endpoint для получения питательной ценности рецепта"""
    recipe = next((r for r in RECIPES if r['id'] == recipe_id), None)
    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404
    
    nutrition_data = calculate_nutrition(recipe)
    
    if "error" in nutrition_data:
        return jsonify(nutrition_data), 500
    
    return jsonify(nutrition_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
