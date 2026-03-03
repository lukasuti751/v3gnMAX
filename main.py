#!/usr/bin/env python3
"""
v3gnMAX — Extended CLI for AI healthy eating lifestyle companion and Veg3n ledger helpers.
Adds random meal/tip/reflection, weekly plan, playbook, kitchen tips, and version.
Usage:
  python v3gnMAX_app.py lookup --meal "oatmeal"
  python v3gnMAX_app.py random-meal
  python v3gnMAX_app.py weekly-plan [--days 7]
  python v3gnMAX_app.py playbook | kitchen-tips | reflection | version
  python v3gnMAX_app.py export-hashes --meal "Oatmeal" --tag "balanced" --type 1 [--file out.json]
  python v3gnMAX_app.py config | constants | stats | demo | interactive
"""

from __future__ import annotations

# v3gnMAX is the extended CLI companion for HealthyPath4Life and the Veg3n contract.
# Meal types: 1=breakfast, 2=lunch, 3=dinner, 4=snack. All hashes are computed locally.

import argparse
import hashlib
import json
import random
import sys
from pathlib import Path

APP_NAME = "v3gnMAX"
V3GNMAX_VERSION = "1.0.0"

# -----------------------------------------------------------------------------
# MEAL DATA (local guide — not medical advice)
# -----------------------------------------------------------------------------

MEALS = [
    {"name": "Oatmeal with berries and nuts", "meal_type": 1, "path_tag": "balanced", "desc": "Whole oats, fresh berries, nuts"},
    {"name": "Scrambled eggs with spinach and toast", "meal_type": 1, "path_tag": "high-protein", "desc": "Eggs, spinach, whole-grain toast"},
    {"name": "Greek yogurt with honey and granola", "meal_type": 1, "path_tag": "balanced", "desc": "Yogurt, honey, granola"},
    {"name": "Green smoothie (kale, banana, almond milk)", "meal_type": 1, "path_tag": "plant-based", "desc": "Kale, banana, almond milk"},
    {"name": "Porridge with banana and cinnamon", "meal_type": 1, "path_tag": "whole-foods", "desc": "Oats, banana, cinnamon"},
    {"name": "Avocado toast with eggs", "meal_type": 1, "path_tag": "balanced", "desc": "Whole-grain bread, avocado, eggs"},
    {"name": "Chia pudding with fruit", "meal_type": 1, "path_tag": "plant-based", "desc": "Chia seeds, plant milk, fruit"},
    {"name": "Whole-grain cereal with milk and berries", "meal_type": 1, "path_tag": "balanced", "desc": "Cereal, milk, berries"},
    {"name": "Omelette with vegetables and cheese", "meal_type": 1, "path_tag": "high-protein", "desc": "Eggs, mixed veg, cheese"},
    {"name": "Pancakes with maple syrup and fruit", "meal_type": 1, "path_tag": "balanced", "desc": "Whole-grain pancakes, syrup, fruit"},
    {"name": "Grilled chicken salad with quinoa", "meal_type": 2, "path_tag": "high-protein", "desc": "Chicken, greens, quinoa"},
    {"name": "Lentil soup with whole-grain bread", "meal_type": 2, "path_tag": "plant-based", "desc": "Lentils, vegetables, bread"},
    {"name": "Salmon with roasted vegetables and brown rice", "meal_type": 3, "path_tag": "balanced", "desc": "Salmon, roasted veg, rice"},
    {"name": "Vegetable stir-fry with tofu", "meal_type": 2, "path_tag": "plant-based", "desc": "Mixed vegetables, tofu"},
    {"name": "Turkey and vegetable skewers", "meal_type": 3, "path_tag": "high-protein", "desc": "Turkey, vegetables"},
    {"name": "Bean chilli with brown rice", "meal_type": 3, "path_tag": "plant-based", "desc": "Beans, tomatoes, rice"},
    {"name": "Baked sweet potato with black beans", "meal_type": 3, "path_tag": "plant-based", "desc": "Sweet potato, black beans"},
    {"name": "Chickpea curry with basmati rice", "meal_type": 3, "path_tag": "plant-based", "desc": "Chickpeas, curry, rice"},
    {"name": "Hummus and vegetable sticks", "meal_type": 4, "path_tag": "whole-foods", "desc": "Hummus, carrots, cucumber"},
    {"name": "Apple with almond butter", "meal_type": 4, "path_tag": "balanced", "desc": "Apple, almond butter"},
    {"name": "Mixed nuts and dried fruit", "meal_type": 4, "path_tag": "whole-foods", "desc": "Nuts, dried fruit"},
    {"name": "Whole-grain wrap with turkey and avocado", "meal_type": 2, "path_tag": "balanced", "desc": "Wrap, turkey, avocado"},
    {"name": "Edamame with sea salt", "meal_type": 4, "path_tag": "plant-based", "desc": "Edamame, salt"},
    {"name": "Trail mix (nuts, seeds, dark chocolate)", "meal_type": 4, "path_tag": "whole-foods", "desc": "Nuts, seeds, chocolate"},
    {"name": "Rice bowl with grilled vegetables", "meal_type": 2, "path_tag": "plant-based", "desc": "Rice, grilled veg"},
    {"name": "Tuna salad with greens", "meal_type": 2, "path_tag": "high-protein", "desc": "Tuna, mixed greens"},
    {"name": "Vegetable soup with whole-grain roll", "meal_type": 2, "path_tag": "low-sugar", "desc": "Vegetable soup, roll"},
    {"name": "Grilled fish with lemon and herbs", "meal_type": 3, "path_tag": "balanced", "desc": "Fish, lemon, herbs"},
    {"name": "Pasta with tomato sauce and vegetables", "meal_type": 3, "path_tag": "plant-based", "desc": "Pasta, tomato, veg"},
    {"name": "Stir-fried chicken with broccoli", "meal_type": 3, "path_tag": "high-protein", "desc": "Chicken, broccoli"},
    {"name": "Quinoa salad with feta and olives", "meal_type": 2, "path_tag": "mediterranean", "desc": "Quinoa, feta, olives"},
    {"name": "Buddha bowl (grains, legumes, veg)", "meal_type": 2, "path_tag": "plant-based", "desc": "Grains, legumes, veg"},
    {"name": "Overnight oats with berries", "meal_type": 1, "path_tag": "meal-prep", "desc": "Oats, berries, soaked overnight"},
    {"name": "Egg muffins with spinach", "meal_type": 1, "path_tag": "meal-prep", "desc": "Eggs, spinach, baked"},
    {"name": "Fruit and nut bar", "meal_type": 4, "path_tag": "whole-foods", "desc": "Dried fruit, nuts"},
    {"name": "Cottage cheese with pineapple", "meal_type": 4, "path_tag": "high-protein", "desc": "Cottage cheese, pineapple"},
    {"name": "Celery with peanut butter", "meal_type": 4, "path_tag": "balanced", "desc": "Celery, peanut butter"},
    {"name": "Roasted vegetable medley", "meal_type": 3, "path_tag": "plant-based", "desc": "Roasted vegetables"},
    {"name": "Lean beef with green beans", "meal_type": 3, "path_tag": "high-protein", "desc": "Beef, green beans"},
    {"name": "Mushroom risotto", "meal_type": 3, "path_tag": "plant-based", "desc": "Rice, mushrooms"},
    {"name": "Cauliflower rice with chicken", "meal_type": 3, "path_tag": "low-carb", "desc": "Cauliflower, chicken"},
    {"name": "Shakshuka with whole-grain bread", "meal_type": 1, "path_tag": "mediterranean", "desc": "Eggs, tomatoes, bread"},
    {"name": "Smoothie bowl with granola", "meal_type": 1, "path_tag": "plant-based", "desc": "Smoothie, granola topping"},
    {"name": "Breakfast burrito with beans", "meal_type": 1, "path_tag": "high-fibre", "desc": "Tortilla, beans, eggs"},
    {"name": "Muesli with milk and fruit", "meal_type": 1, "path_tag": "whole-foods", "desc": "Muesli, milk, fruit"},
    {"name": "Veggie wrap with hummus", "meal_type": 2, "path_tag": "plant-based", "desc": "Wrap, hummus, vegetables"},
    {"name": "Minestrone soup", "meal_type": 2, "path_tag": "plant-based", "desc": "Vegetable and bean soup"},
    {"name": "Grilled vegetable sandwich", "meal_type": 2, "path_tag": "plant-based", "desc": "Grilled veg, bread"},
    {"name": "Salmon poke bowl", "meal_type": 2, "path_tag": "balanced", "desc": "Salmon, rice, vegetables"},
    {"name": "Stuffed bell peppers", "meal_type": 3, "path_tag": "plant-based", "desc": "Peppers, rice, beans"},
    {"name": "Lamb curry with rice", "meal_type": 3, "path_tag": "balanced", "desc": "Lamb, curry, rice"},
    {"name": "Vegetable lasagne", "meal_type": 3, "path_tag": "plant-based", "desc": "Pasta, vegetables, cheese"},
    {"name": "Baked cod with herbs", "meal_type": 3, "path_tag": "balanced", "desc": "Cod, herbs"},
    {"name": "Peanut butter and banana toast", "meal_type": 1, "path_tag": "balanced", "desc": "Bread, peanut butter, banana"},
    {"name": "Cottage cheese with peach", "meal_type": 1, "path_tag": "high-protein", "desc": "Cottage cheese, peach"},
    {"name": "Breakfast quinoa with nuts", "meal_type": 1, "path_tag": "whole-foods", "desc": "Quinoa, nuts"},
    {"name": "Veggie frittata", "meal_type": 1, "path_tag": "high-protein", "desc": "Eggs, vegetables"},
    {"name": "Rice cake with avocado", "meal_type": 1, "path_tag": "balanced", "desc": "Rice cake, avocado"},
    {"name": "Smoothie with spinach and mango", "meal_type": 1, "path_tag": "plant-based", "desc": "Spinach, mango"},
    {"name": "Bagel with cream cheese and salmon", "meal_type": 1, "path_tag": "high-protein", "desc": "Bagel, cream cheese, salmon"},
    {"name": "French toast with berries", "meal_type": 1, "path_tag": "balanced", "desc": "Bread, egg, berries"},
    {"name": "Black bean tacos", "meal_type": 2, "path_tag": "plant-based", "desc": "Tortillas, black beans"},
    {"name": "Grilled cheese and tomato soup", "meal_type": 2, "path_tag": "balanced", "desc": "Cheese, bread, soup"},
    {"name": "Falafel wrap with tahini", "meal_type": 2, "path_tag": "plant-based", "desc": "Falafel, wrap, tahini"},
    {"name": "Sushi roll with brown rice", "meal_type": 2, "path_tag": "balanced", "desc": "Rice, fish, vegetables"},
    {"name": "Caprese salad with balsamic", "meal_type": 2, "path_tag": "mediterranean", "desc": "Mozzarella, tomato, basil"},
    {"name": "Peanut noodles with vegetables", "meal_type": 2, "path_tag": "plant-based", "desc": "Noodles, peanut sauce, veg"},
    {"name": "Turkey chilli", "meal_type": 2, "path_tag": "high-protein", "desc": "Turkey, beans, tomatoes"},
    {"name": "Spinach and ricotta cannelloni", "meal_type": 3, "path_tag": "plant-based", "desc": "Pasta, spinach, ricotta"},
    {"name": "Shepherd's pie with sweet potato", "meal_type": 3, "path_tag": "balanced", "desc": "Minced meat, sweet potato"},
    {"name": "Thai green curry with rice", "meal_type": 3, "path_tag": "balanced", "desc": "Curry, rice"},
    {"name": "Grilled prawns with garlic", "meal_type": 3, "path_tag": "high-protein", "desc": "Prawns, garlic"},
    {"name": "Lentil shepherd's pie", "meal_type": 3, "path_tag": "plant-based", "desc": "Lentils, potato topping"},
    {"name": "Ratatouille with crusty bread", "meal_type": 3, "path_tag": "plant-based", "desc": "Vegetables, bread"},
    {"name": "Pork tenderloin with apples", "meal_type": 3, "path_tag": "balanced", "desc": "Pork, apples"},
    {"name": "Vegetable curry with naan", "meal_type": 3, "path_tag": "plant-based", "desc": "Curry, naan"},
    {"name": "Beef and broccoli stir-fry", "meal_type": 3, "path_tag": "high-protein", "desc": "Beef, broccoli"},
    {"name": "Stuffed squash with quinoa", "meal_type": 3, "path_tag": "plant-based", "desc": "Squash, quinoa"},
    {"name": "Greek salad with grilled chicken", "meal_type": 2, "path_tag": "mediterranean", "desc": "Greens, chicken, feta"},
    {"name": "Rice and dal", "meal_type": 3, "path_tag": "plant-based", "desc": "Rice, lentils"},
    {"name": "Popcorn with nutritional yeast", "meal_type": 4, "path_tag": "whole-foods", "desc": "Popcorn, yeast"},
    {"name": "Rice crackers with hummus", "meal_type": 4, "path_tag": "plant-based", "desc": "Crackers, hummus"},
    {"name": "Banana with oats", "meal_type": 4, "path_tag": "balanced", "desc": "Banana, oats"},
    {"name": "Cheese and grapes", "meal_type": 4, "path_tag": "balanced", "desc": "Cheese, grapes"},
    {"name": "Veggie sticks with guacamole", "meal_type": 4, "path_tag": "plant-based", "desc": "Vegetables, guacamole"},
    {"name": "Hard-boiled eggs", "meal_type": 4, "path_tag": "high-protein", "desc": "Eggs"},
    {"name": "Protein shake", "meal_type": 4, "path_tag": "high-protein", "desc": "Protein powder, milk"},
    {"name": "Dates with almond butter", "meal_type": 4, "path_tag": "whole-foods", "desc": "Dates, almond butter"},
    {"name": "Yogurt parfait", "meal_type": 4, "path_tag": "balanced", "desc": "Yogurt, granola, fruit"},
    {"name": "Seaweed snacks", "meal_type": 4, "path_tag": "low-carb", "desc": "Seaweed"},
    {"name": "Olives and cheese", "meal_type": 4, "path_tag": "mediterranean", "desc": "Olives, cheese"},
    {"name": "Apple slices with cinnamon", "meal_type": 4, "path_tag": "low-sugar", "desc": "Apple, cinnamon"},
    {"name": "Roasted chickpeas", "meal_type": 4, "path_tag": "plant-based", "desc": "Chickpeas"},
    {"name": "Cucumber with tzatziki", "meal_type": 4, "path_tag": "mediterranean", "desc": "Cucumber, tzatziki"},
    {"name": "Dark chocolate square", "meal_type": 4, "path_tag": "mindful", "desc": "Dark chocolate"},
    {"name": "Berry mix", "meal_type": 4, "path_tag": "whole-foods", "desc": "Mixed berries"},
    {"name": "Kale chips", "meal_type": 4, "path_tag": "plant-based", "desc": "Kale"},
    {"name": "Pumpkin seeds", "meal_type": 4, "path_tag": "whole-foods", "desc": "Seeds"},
    {"name": "Rice pudding with raisins", "meal_type": 1, "path_tag": "balanced", "desc": "Rice, milk, raisins"},
    {"name": "Breakfast burrito bowl", "meal_type": 1, "path_tag": "high-protein", "desc": "Eggs, beans, veg"},
    {"name": "Buckwheat porridge", "meal_type": 1, "path_tag": "whole-foods", "desc": "Buckwheat"},
    {"name": "Smoked salmon and cream cheese", "meal_type": 1, "path_tag": "high-protein", "desc": "Salmon, cream cheese"},
    {"name": "Breakfast salad with egg", "meal_type": 1, "path_tag": "balanced", "desc": "Greens, egg"},
    {"name": "Sweet potato hash", "meal_type": 1, "path_tag": "whole-foods", "desc": "Sweet potato"},
    {"name": "Tofu scramble", "meal_type": 1, "path_tag": "plant-based", "desc": "Tofu"},
    {"name": "Millet porridge with fruit", "meal_type": 1, "path_tag": "plant-based", "desc": "Millet, fruit"},
    {"name": "Breakfast bowl (acai style)", "meal_type": 1, "path_tag": "plant-based", "desc": "Fruit, granola"},
    {"name": "Egg and soldiers", "meal_type": 1, "path_tag": "balanced", "desc": "Egg, bread"},
    {"name": "Congee with ginger", "meal_type": 1, "path_tag": "whole-foods", "desc": "Rice porridge, ginger"},
    {"name": "Breakfast pizza (whole grain)", "meal_type": 1, "path_tag": "balanced", "desc": "Base, egg, veg"},
    {"name": "Lox and bagel", "meal_type": 1, "path_tag": "high-protein", "desc": "Salmon, bagel"},
    {"name": "Pumpkin oatmeal", "meal_type": 1, "path_tag": "plant-based", "desc": "Oats, pumpkin"},
    {"name": "Breakfast quesadilla", "meal_type": 1, "path_tag": "high-protein", "desc": "Tortilla, cheese, egg"},
    {"name": "Fruit salad with mint", "meal_type": 1, "path_tag": "plant-based", "desc": "Mixed fruit, mint"},
    {"name": "Corn fritters with avocado", "meal_type": 1, "path_tag": "balanced", "desc": "Corn, avocado"},
    {"name": "Baked oats with berries", "meal_type": 1, "path_tag": "meal-prep", "desc": "Oats, berries"},
    {"name": "Breakfast sausage and eggs", "meal_type": 1, "path_tag": "high-protein", "desc": "Sausage, eggs"},
    {"name": "Cream of wheat with honey", "meal_type": 1, "path_tag": "balanced", "desc": "Wheat, honey"},
    {"name": "Breakfast sandwich (whole grain)", "meal_type": 1, "path_tag": "balanced", "desc": "Bread, egg, cheese"},
    {"name": "Mango and coconut chia", "meal_type": 1, "path_tag": "plant-based", "desc": "Chia, mango, coconut"},
]

PATH_TAGS = [
    {"id": "balanced", "label": "Balanced", "desc": "Mix of macros, three meals plus snacks"},
    {"id": "plant-based", "label": "Plant-based", "desc": "Focus on plants"},
    {"id": "high-protein", "label": "High protein", "desc": "Protein at each meal"},
    {"id": "low-sugar", "label": "Low sugar", "desc": "Minimise added sugars"},
    {"id": "meal-prep", "label": "Meal prep", "desc": "Prepared ahead"},
    {"id": "mindful", "label": "Mindful", "desc": "Mindful eating focus"},
    {"id": "whole-foods", "label": "Whole foods", "desc": "Minimally processed"},
    {"id": "mediterranean", "label": "Mediterranean", "desc": "Mediterranean style"},
    {"id": "low-carb", "label": "Low carb", "desc": "Lower carbohydrate"},
    {"id": "high-fibre", "label": "High fibre", "desc": "High fibre focus"},
    {"id": "breakfast-club", "label": "Breakfast club", "desc": "Morning meal focus"},
    {"id": "lunch-goals", "label": "Lunch goals", "desc": "Midday meal focus"},
    {"id": "dinner-balance", "label": "Dinner balance", "desc": "Evening meal focus"},
    {"id": "snack-smart", "label": "Snack smart", "desc": "Healthy snacks"},
    {"id": "flexitarian", "label": "Flexitarian", "desc": "Mostly plants, some animal"},
]

# Additional meal description strings for hashing (expand as needed)
MEAL_DESCRIPTIONS = [
    "Oatmeal with berries and nuts", "Scrambled eggs with spinach and toast", "Greek yogurt with honey and granola",
    "Green smoothie kale banana almond milk", "Porridge with banana and cinnamon", "Avocado toast with eggs",
    "Chia pudding with fruit", "Whole-grain cereal with milk and berries", "Omelette with vegetables and cheese",
    "Pancakes with maple syrup and fruit", "Grilled chicken salad with quinoa", "Lentil soup with whole-grain bread",
    "Salmon with roasted vegetables and brown rice", "Vegetable stir-fry with tofu", "Turkey and vegetable skewers",
    "Bean chilli with brown rice", "Baked sweet potato with black beans", "Chickpea curry with basmati rice",
    "Hummus and vegetable sticks", "Apple with almond butter", "Mixed nuts and dried fruit",
    "Whole-grain wrap with turkey and avocado", "Edamame with sea salt", "Trail mix nuts seeds dark chocolate",
    "Rice bowl with grilled vegetables", "Tuna salad with greens", "Vegetable soup with whole-grain roll",
    "Grilled fish with lemon and herbs", "Pasta with tomato sauce and vegetables", "Stir-fried chicken with broccoli",
    "Quinoa salad with feta and olives", "Buddha bowl grains legumes veg", "Overnight oats with berries",
    "Egg muffins with spinach", "Fruit and nut bar", "Cottage cheese with pineapple", "Celery with peanut butter",
    "Roasted vegetable medley", "Lean beef with green beans", "Mushroom risotto", "Cauliflower rice with chicken",
    "Shakshuka with whole-grain bread", "Smoothie bowl with granola", "Breakfast burrito with beans",
    "Muesli with milk and fruit", "Veggie wrap with hummus", "Minestrone soup", "Grilled vegetable sandwich",
    "Salmon poke bowl", "Stuffed bell peppers", "Lamb curry with rice", "Vegetable lasagne", "Baked cod with herbs",
    "Pork tenderloin with apples", "Vegetable curry with naan", "Beef and broccoli stir-fry", "Stuffed squash with quinoa",
    "Greek salad with grilled chicken", "Rice and dal", "Popcorn with nutritional yeast", "Rice crackers with hummus",
    "Banana with oats", "Cheese and grapes", "Veggie sticks with guacamole", "Hard-boiled eggs", "Protein shake",
    "Dates with almond butter", "Yogurt parfait", "Seaweed snacks", "Olives and cheese", "Apple slices with cinnamon",
    "Roasted chickpeas", "Cucumber with tzatziki", "Dark chocolate square", "Berry mix", "Kale chips", "Pumpkin seeds",
]
for i in range(100):
    MEAL_DESCRIPTIONS.append(f"Custom meal description {i+1} for logging")

# Usage examples (long reference)
USAGE_EXAMPLES = """
# Hash a meal description for logMeal
python v3gn_app.py hash --text "Oatmeal with berries"
# Output: 0x...

# Hash a path tag
python v3gn_app.py hash --text "balanced"
# Output: 0x...

# Export hashes for logMeal(mealHash, pathTag, mealType)
python v3gn_app.py export-hashes --meal "Oatmeal with berries" --tag "balanced" --type 1
# Output: {"mealHash": "0x...", "pathTag": "0x...", "mealType": 1}

# Export to file
python v3gn_app.py export-hashes --meal "Salmon with vegetables" --tag "high-protein" --type 3 --file hashes.json

# Lookup meals by name
python v3gn_app.py lookup --meal "oatmeal"

# Lookup by path tag
python v3gn_app.py lookup --path-tag "plant-based"

# Lookup by meal type (1=breakfast, 2=lunch, 3=dinner, 4=snack)
python v3gn_app.py lookup --type 1

# Suggest meals for a keyword
python v3gn_app.py suggest breakfast

# List all meals
python v3gn_app.py list-meals

# List path tags
python v3gn_app.py list-paths

# List tips
python v3gn_app.py list-tips

# Meals by type
python v3gn_app.py meals-by-type --type 1

# Meals by tag
python v3gn_app.py meals-by-tag --tag balanced

# Config and constants
python v3gn_app.py config
python v3gn_app.py constants

# Stats
python v3gn_app.py stats

# Demo
python v3gn_app.py demo

# Interactive REPL
python v3gn_app.py interactive

# Help and reference
python v3gn_app.py help
python v3gn_app.py reference
python v3gn_app.py examples
"""

# Contract ABI snippet for front-end integration (key functions only)
CONTRACT_ABI_SNIPPET = [
    '{"type":"function","name":"getCompanionDigest","inputs":[],"outputs":[{"name":"totalMeals","type":"uint256"},{"name":"totalPaths","type":"uint256"},{"name":"totalTips","type":"uint256"},{"name":"deployBlockNum","type":"uint256"},{"name":"paused","type":"bool"}]}',
    '{"type":"function","name":"getMeal","inputs":[{"name":"mealId","type":"uint256"}],"outputs":[{"name":"user","type":"address"},{"name":"mealHash","type":"bytes32"},{"name":"pathTag","type":"bytes32"},{"name":"loggedAtBlock","type":"uint256"},{"name":"mealType","type":"uint8"},{"name":"active","type":"bool"}]}',
    '{"type":"function","name":"pointsBalance","inputs":[{"name":"","type":"address"}],"outputs":[{"name":"","type":"uint256"}]}',
    '{"type":"function","name":"logMeal","inputs":[{"name":"mealHash","type":"bytes32"},{"name":"pathTag","type":"bytes32"},{"name":"mealType","type":"uint8"}],"outputs":[{"name":"mealId","type":"uint256"}]}',
    '{"type":"function","name":"getMealIds","inputs":[],"outputs":[{"name":"","type":"uint256[]"}]}',
    '{"type":"function","name":"getPathIds","inputs":[],"outputs":[{"name":"","type":"uint256[]"}]}',
    '{"type":"function","name":"getConstants","inputs":[],"outputs":[{"name":"bpsBase","type":"uint256"},{"name":"maxMeals","type":"uint256"},{"name":"maxPaths","type":"uint256"},{"name":"maxTips","type":"uint256"},{"name":"maxBatchMeals","type":"uint256"},{"name":"pointsScale","type":"uint256"}]}',
]

# Meal type reference table (for docs)
MEAL_TYPE_REFERENCE = """
Meal type | Contract constant       | Label
----------|-------------------------|--------
    1     | V3G_MEAL_BREAKFAST      | breakfast
    2     | V3G_MEAL_LUNCH          | lunch
    3     | V3G_MEAL_DINNER         | dinner
    4     | V3G_MEAL_SNACK          | snack

Use --type 1, 2, 3 or 4 in export-hashes and when calling logMeal(mealHash, pathTag, mealType).
"""

# Path tag reference (ids for hashing)
PATH_TAG_REFERENCE = """
balanced | plant-based | high-protein | low-sugar | meal-prep | mindful
whole-foods | mediterranean | low-carb | high-fibre | breakfast-club | lunch-goals
dinner-balance | snack-smart | flexitarian
"""

# Additional meals for extended database (name, type, tag, desc)
ADDITIONAL_MEALS = []
for t in range(1, 5):
    for tag in ["balanced", "plant-based", "high-protein"]:
        for i in range(8):
            ADDITIONAL_MEALS.append({
                "name": f"Meal {tag} {MEAL_TYPE_LABELS[t]} {i+1}",
                "meal_type": t,
                "path_tag": tag,
                "desc": f"Description for {tag} {MEAL_TYPE_LABELS[t]} {i+1}",
            })

TIPS = [
    "Eat whole foods: vegetables, fruits, whole grains, legumes, lean proteins.",
    "Stay hydrated. Drink water with meals.",
    "Balance meals: combine protein, fibre and healthy fats.",
    "Plan ahead. Meal prep helps on busy days.",
    "Eat mindfully. Pay attention to hunger and fullness.",
    "Limit highly processed foods and added sugars.",
    "Use reasonable portions.",
    "Keep consistent meal times when possible.",
    "Eat a variety of colours and types of produce.",
    "Good sleep and stress management support eating habits.",
    "Include protein at breakfast for sustained energy.",
    "Add vegetables to at least two meals per day.",
    "Choose whole grains over refined when you can.",
    "Snack on nuts, fruit or yogurt rather than processed options.",
    "Cook at home more often to control ingredients and portions.",
    "Use the path tag 'balanced' for mixed macros.",
    "Log snacks as meal type 4 for a complete daily picture.",
    "Join a path that matches your goal (e.g. plant-based, high-protein).",
    "Start the day with fibre and protein (e.g. oats, eggs).",
    "Limit sugary drinks; opt for water, tea or black coffee.",
    "Eat slowly and stop when you feel comfortably full.",
    "Prefer unsaturated fats (olive oil, nuts, avocado).",
    "Include legumes (beans, lentils) for fibre and protein.",
    "Vary your protein sources: fish, poultry, legumes, tofu.",
    "Use herbs and spices instead of excess salt.",
    "Plan weekly meals to reduce last-minute unhealthy choices.",
    "Keep healthy snacks visible (fruit bowl, nuts).",
    "Read labels to check added sugar and sodium.",
    "Eat with others when possible for social and mindful eating.",
    "Stay active; physical activity supports appetite regulation.",
]

MEAL_TYPE_LABELS = {1: "breakfast", 2: "lunch", 3: "dinner", 4: "snack"}

HELP_TEXT = """
v3gnMAX — AI healthy eating lifestyle companion CLI (extended)
=============================================================

Commands:
  lookup --meal <name>       Lookup meals by name (partial match).
  lookup --path-tag <tag>    Lookup meals by path tag (e.g. balanced, plant-based).
  lookup --type <1-4>       Lookup by meal type: 1=breakfast, 2=lunch, 3=dinner, 4=snack.
  list-meals                List all meals (name, type, path_tag).
  list-paths                List path tags (id, label, desc).
  list-tips                 List healthy eating tips.
  hash --text <string>      Compute keccak256 hash (0x + hex) for contract use.
  hash-batch --meals "a,b"  Hash multiple meal descriptions; --tags "x,y" for path tags.
  suggest <keyword>         Suggest meals matching keyword (name, path_tag, desc).
  export-hashes --meal X --tag Y [--type 1] [--file out.json]
                            Export mealHash, pathTag, mealType for logMeal().
  random-meal [--type 1-4] [--path-tag TAG]  Pick a random meal (v3gnMAX).
  weekly-plan [--days 7] [--seed N]          Generate a weekly meal plan (v3gnMAX).
  playbook                  Print daily practice playbook (v3gnMAX).
  kitchen-tips              Print kitchen flow tips (v3gnMAX).
  reflection                Print a random mindful eating reflection (v3gnMAX).
  version                   Print v3gnMAX version.
  config                    Show app config (meal count, path count, etc.).
  constants                 Show Veg3n contract constant reference.
  stats                     Show meal/path/tip counts and breakdown by type and tag.
  demo                      Run a short demo (lookup, hash examples).
  interactive               Start REPL (lookup, list, hash, suggest, random-meal, reflection, quit).
  help                      Show this help.

Meal types (Veg3n contract):
  1 = V3G_MEAL_BREAKFAST
  2 = V3G_MEAL_LUNCH
  3 = V3G_MEAL_DINNER
  4 = V3G_MEAL_SNACK

Path tags: balanced, plant-based, high-protein, low-sugar, meal-prep, mindful,
  whole-foods, mediterranean, low-carb, high-fibre, breakfast-club, lunch-goals,
  dinner-balance, snack-smart, flexitarian.

Contract: Use export-hashes to get mealHash and pathTag (bytes32). Then call
  contract.logMeal(mealHash, pathTag, mealType) with type 1-4.
"""

# Example log entries for reference (meal desc, path tag, type)
EXAMPLE_LOGS = [
    {"meal": "Oatmeal with berries and nuts", "tag": "balanced", "type": 1},
    {"meal": "Scrambled eggs with spinach and toast", "tag": "high-protein", "type": 1},
    {"meal": "Greek yogurt with honey and granola", "tag": "balanced", "type": 1},
    {"meal": "Green smoothie (kale, banana, almond milk)", "tag": "plant-based", "type": 1},
    {"meal": "Grilled chicken salad with quinoa", "tag": "high-protein", "type": 2},
    {"meal": "Lentil soup with whole-grain bread", "tag": "plant-based", "type": 2},
    {"meal": "Salmon with roasted vegetables and brown rice", "tag": "balanced", "type": 3},
    {"meal": "Vegetable stir-fry with tofu", "tag": "plant-based", "type": 2},
    {"meal": "Hummus and vegetable sticks", "tag": "whole-foods", "type": 4},
    {"meal": "Apple with almond butter", "tag": "balanced", "type": 4},
]

# Extended reference: Veg3n contract methods (for copy-paste or docs)
EXTENDED_REFERENCE = """
Veg3n contract — view functions (read-only):
  getCompanionDigest() -> totalMeals, totalPaths, totalTips, deployBlockNum, paused
  getMeal(mealId) -> user, mealHash, pathTag, loggedAtBlock, mealType, active
  pointsBalance(address) -> uint256
  getMealIds() -> uint256[]
  getPathIds() -> uint256[]
  getConstants() -> bpsBase, maxMeals, maxPaths, maxTips, maxBatchMeals, pointsScale
  getPath(pathId) -> pathTag, startBlock, endBlock, participantCount, exists
  getPathParticipants(pathId) -> address[]
  getActivePathIds() -> uint256[]
  getMealsPaginated(offset, limit) -> ids, users, mealHashes, activeFlags
  getTipIds() -> uint256[]
  getCompanionDomain() -> bytes32
  getImmutables() -> coordinatorAddr, vaultAddr, keeperAddr
  getLatestMealIds(maxCount) -> uint256[]
  getMealCountByUser(user) -> uint256
  getActiveMealCount() -> uint256
  isPathActive(pathId) -> bool
  getMealsByUserPaginated(user, offset, limit) -> uint256[]
  getPointsForAddresses(addresses[]) -> uint256[]
  getTotalPointsInCirculation() -> uint256
  getDailyStreak(user) -> uint256
  getLastLogBlock(user) -> uint256
  getUserGoal(user) -> goalHash, targetValue, setAtBlock

Veg3n contract — state-changing (require signer):
  logMeal(mealHash, pathTag, mealType) -> mealId  // mealType 1-4
  batchLogMeals(mealHashes[], pathTags[], mealTypes[]) -> mealIds[]
  joinPath(pathId)
  leavePath(pathId)
  setGoal(goalHash, targetValue)
  redeemPoints(amount, reasonHash)
  removeMeal(mealId)  // user or reward keeper

Path coordinator only:
  createPath(pathTag, startBlock, endBlock) -> pathId
  recordTip(tipHash) -> tipId
  setPathTagLabel(pathTag, labelHash)

Reward keeper only:
  awardPoints(user, amount)
  awardPointsForMeal(mealId)
  batchAwardPoints(users[], amounts[])
  recordDailySnapshot(user, dayBlock, mealCount, pointsEarned) -> snapshotId

Owner only:
  setCompanionPaused(paused)
  setPointsPerMeal(newPoints)

Errors (revert with custom error): V3G_ZeroAddress, V3G_InvalidMealId, V3G_MealNotFound,
  V3G_InvalidMealHash, V3G_NotPathCoordinator, V3G_NotRewardKeeper, V3G_CompanionPaused,
  V3G_ReentrantCall, V3G_ZeroAmount, V3G_InsufficientPoints, V3G_MaxMealsReached,
  V3G_ArrayLengthMismatch, V3G_BatchTooLarge, V3G_ZeroBatchSize, V3G_PathNotFound,
  V3G_PathNotActive, V3G_AlreadyOnPath, V3G_NotOnPath, V3G_MaxPathsReached,
  V3G_InvalidBlockRange, V3G_InvalidMealType, V3G_TipNotFound, V3G_MaxTipsReached,
  V3G_NotMealUser, V3G_MealAlreadyRemoved, V3G_InvalidLabelHash.
"""

HEALTHY_PRACTICE_PLAYBOOK = """
HealthyPath4Life — daily practice ideas for v3gn users

- Start the day by drinking a glass of water before coffee.
- Take one deep breath before every bite at breakfast.
- Check in with hunger and fullness on a simple 1-10 scale.
- Plan one plant-forward meal before lunchtime.
- Add a handful of vegetables to your usual breakfast.
- Swap one sugary drink for water, tea or sparkling water.
- Pack a balanced snack before leaving home.
- Pre-log a meal idea into v3gn before you cook it.
- Reflect briefly on yesterday’s meals without judgement.
- Walk for five minutes after your largest meal.
- Choose one food you want to add in, not just remove.
- Eat one meal today away from screens.
- Include at least one source of fibre in each meal.
- Keep a bowl of fruit visible on the counter.
- Carry a small reusable water bottle with you.
- Try a new vegetable or fruit you rarely buy.
- Make half of your plate vegetables at dinner.
- Include a protein source at every main meal.
- Use smaller plates if you tend to over-serve.
- Pause halfway through meals to reassess hunger.
- Add a side salad instead of fries once this week.
- Roast a tray of mixed vegetables for easy add-ons.
- Freeze individual portions of a favourite soup.
- Use herbs and spices to cut back on salt.
- Keep nuts or seeds on hand for quick snacks.
- Pre-cut vegetables for easy grab-and-go snacking.
- Schedule a recurring reminder to log meals.
- Save three go-to breakfasts inside your own notes.
- Pair fruit with protein or healthy fat for snacks.
- Try to eat at roughly similar times each day.
- Give yourself permission to enjoy food without guilt.
- Use v3gn to explore meal ideas by path tag.
- Add a small side of beans or lentils to dinner.
- Try a meatless Monday or plant-focused evening meal.
- Plan tomorrow’s breakfast before going to bed.
- Write down three reasons you care about your health.
- Choose whole fruit over fruit juice where possible.
- Try swapping white rice for brown or mixed grains.
- Include a colourful vegetable you enjoy, not just “shoulds”.
- Add a spoonful of yogurt on spicy or rich meals.
- Keep a simple list of pantry staples you like.
- Build a “default” balanced plate formula for yourself.
- Prepare overnight oats for mornings when you are rushed.
- Pack leftovers for lunch instead of skipping meals.
- Practice putting your fork down between bites.
- Notice how different meals make your energy feel.
- Eat at a table, even if you are alone.
- Add a side of vegetables to take-away meals.
- Try baking instead of frying when possible.
- Keep a small note of meals that feel satisfying.
- Use frozen vegetables for quick additions.
- Store cut fruit in see-through containers at eye level.
- Sit down to eat, rather than standing or walking.
- Limit work at the computer while snacking.
- Play calm music during dinner to slow your pace.
- Start meals with a few bites of vegetables.
- Share a meal idea with a friend for accountability.
- Celebrate small wins, such as one extra glass of water.
- Notice stress or boredom before reaching for food.
- Take three slow breaths before opening the fridge.
- Drink water between alcoholic beverages if you drink.
- Choose grilled or baked options when eating out.
- Ask for dressings on the side to control portions.
- Add legumes to salads for extra protein and fibre.
- Keep easy protein like boiled eggs in the fridge.
- Switch to whole-grain bread if you enjoy it.
- Slice vegetables into sticks for quick nibbling.
- Explore herbs like basil, coriander or dill for flavour.
- Experiment with spice blends to keep meals interesting.
- Try one new healthy recipe per week.
- Keep a backup freezer meal for busy nights.
- Use leftovers creatively (e.g. bowls, wraps, salads).
- Batch cook whole grains and refrigerate or freeze.
- Portion trail mix into small containers in advance.
- Pack snacks in your work or study bag every Sunday.
- Reflect weekly on what worked and what did not.
- Focus on progress over perfection.
- Use v3gn stats to see your most common meal types.
- Log at least one meal even on “off” days.
- Attach a simple habit to something you already do.
- Give yourself unconditional permission to eat enough.
- Notice language around “good” or “bad” foods.
- Reframe restrictive thoughts into supportive ones.
- Highlight how meals support energy, focus and mood.
- Create a relaxed pre-meal ritual (water, breath, gratitude).
- Eat seated with both feet on the floor when possible.
- Put tempting snacks behind other foods, not in front.
- Store sliced vegetables at eye level in the fridge.
- Place sweets in an opaque container out of sight.
- Keep a small bowl for measured crunchy snacks.
- Pair a show or podcast only with main meals, not grazing.
- Leave a glass by the sink as a water cue.
- Record how certain meals affect sleep.
- Try to finish dinners at least two hours before bed.
- Add magnesium-rich foods like greens and nuts.
- Make a habit of adding a plant-based food to each plate.
- Keep a list of quick meal ideas that use pantry items.
- Use canned beans and tomatoes for easy curries and chilli.
- Try a simple homemade dressing instead of bottled ones.
- Freeze ripe bananas for smoothies and snacks.
- Pre-portion smoothie packs in freezer bags.
- Include a vegetable or fruit at breakfast three days in a row.
- Track streaks in v3gn for fun, not punishment.
- Plan grocery shopping after a snack, not when hungry.
- Eat a small snack before events with many desserts.
- Serve yourself away from serving dishes, then sit.
- Check in with fullness before reaching for seconds.
- Enjoy favourite foods slowly and mindfully when you choose them.
- Keep emergency snacks in your car or bag.
- Try herbal tea after dinner instead of extra dessert.
- Separate boredom from hunger by pausing 10 minutes.
- Keep a short list of non-food comfort activities.
- Notice which meals fuel great workouts or walks.
- Add a source of protein after strength sessions.
- Include carbohydrates before intense activity.
- Balance high-fat meals with extra vegetables.
- Avoid labelling whole days as “ruined” by one meal.
- Set flexible ranges rather than strict rules.
- Use neutral language like “more” and “less” instead of “never”.
- Ask what support future-you might appreciate.
- Practice saying no kindly at social events when full.
- Bring a dish you enjoy to gatherings when possible.
- Focus on connection instead of only food at events.
- Eat a small snack before grocery shopping.
- Avoid scrolling on your phone during meals.
- Drink water while cooking to stay hydrated.
- Keep a reusable container for leftovers ready.
- Freeze single portions of cooked grains.
- Label containers with dates and simple descriptions.
- Rotate different colours of vegetables each week.
- Experiment with breakfast-for-dinner occasionally.
- Keep spices labelled and visible for quick use.
- Prepare a simple vegetable soup base and customise later.
- Pre-chop onions and garlic for quick cooking.
- Saute extra vegetables for tomorrow’s omelette.
- Add seeds to salads, soups or yoghurt.
- Choose a gentle pace of change rather than an overhaul.
- Celebrate consistency, not just novelty.
- Tune in to how caffeine affects your appetite and sleep.
- Pause notifications during mealtimes when possible.
- Charge your phone away from the table.
- Consider adding a multicolour salad once a week.
- Try including fermented foods if you like them.
- Encourage yourself the way you would a friend.
- Keep a small notebook for meal ideas and reflections.
- Allow flexible portions that match your hunger.
- Keep low-effort frozen vegetables on hand.
- Use pre-washed greens if it helps you eat more veggies.
- Add fruit to water if it encourages hydration.
- Pack cut citrus or apples for portable snacks.
- Keep a checklist of habits inside a cupboard door.
- Revisit your goals every month in light of real life.
- Aim for gentle consistency over perfect tracking.
- Acknowledge that some days will be off-plan.
- Return to one tiny anchor habit on tricky days.
- Use v3gn to log the meals that feel best in your body.
- Share anonymised patterns with your healthcare team if needed.
- Let curiosity guide your logs instead of criticism.
- Write one sentence about how a meal made you feel.
- Use colours and textures to make plates more appealing.
- Plate meals before tasting rather than snacking while cooking.
- Close the kitchen at a set time if helpful for you.
- Keep a favourite mug or bowl reserved for breakfast rituals.
- Replace all-or-nothing thinking with flexible options.
- Give yourself credit for every step toward nourishment.
"""

KITCHEN_FLOW_IDEAS = """
HealthyPath4Life — kitchen flow and environment ideas

- Keep your cutting board and favourite knife easily accessible.
- Store everyday spices near the stove in a visible rack.
- Dedicate one shelf in your fridge to ready-to-eat vegetables.
- Keep whole grains like oats, rice and quinoa in labelled jars.
- Place healthy snack options at the front of cupboards.
- Move less supportive snacks to higher, less visible shelves.
- Keep a small compost bin or bowl on the counter while chopping.
- Prepare ingredients for multiple meals in a single session.
- Chop extra onions and garlic and store them in airtight containers.
- Batch roast root vegetables for use across different meals.
- Group breakfast items together in one “morning zone”.
- Group tea, coffee and mugs in a calm beverage station.
- Place water glasses near the sink or filter.
- Use clear containers so you can see vegetables and leftovers.
- Label containers with the date and simple meal notes.
- Keep a notepad or whiteboard on the fridge for quick ideas.
- Store a basic set of measuring cups and spoons together.
- Keep a clean towel or cloth handy while cooking.
- Tidy surfaces briefly before starting to cook a meal.
- Pre-read simple recipes before beginning to cook.
- Lay out all ingredients before turning on the stove.
- Clean while you cook to keep surfaces uncluttered.
- Keep a small bowl for food scraps while chopping.
- Group pantry items by function (baking, grains, snacks).
- Rotate older ingredients to the front of shelves.
- Dedicate a small box to quick-meal ingredients.
- Keep canned beans, tomatoes and fish within reach.
- Store oils and vinegars together in a stable place.
- Use oven timers and phone reminders to prevent burning food.
- Keep a spare set of kitchen scissors dedicated to food.
- Arrange frequently used tools in the top drawer.
- Choose a few versatile pans rather than many specialised ones.
- Keep a strainer or colander near the sink.
- Stack cutting boards vertically for easy access.
- Place a fruit bowl in the centre of the table.
- Set up a simple salad station with tongs and a large bowl.
- Store sharp knives safely and have them sharpened periodically.
- Keep a safe step stool if cupboards are high.
- Make space for a comfortable chopping posture.
- Adjust lighting if possible to make the kitchen inviting.
- Open a window when cooking strong-smelling foods.
- Keep a small speaker or playlist for relaxed cooking music.
- Clear a small zone specifically for packing lunches.
- Prepare reusable containers and lids before portioning leftovers.
- Assign a shelf in the freezer for prepared meals.
- Pre-portion snacks into individual containers at the start of the week.
- Store spices you rarely use separately from core seasonings.
- Keep hot pads or oven mitts easy to grab.
- Wrap herbs in slightly damp towels to prolong freshness.
- Freeze washed and trimmed greens if they begin to wilt.
- Use glass jars for soups and stews when storing or freezing.
- Label frozen meals with contents and reheating notes.
- Group smoothie ingredients together in the freezer.
- Set up a simple smoothie station near the blender.
- Keep knives away from clutter to support safe chopping.
- Place chopping boards near the sink for quick rinsing.
- Keep dish soap and a brush clearly visible.
- Run a quick sink of soapy water before starting to cook.
- Soak pots and pans promptly after use.
- Wipe down stove surfaces once they are cool.
- Organise spices alphabetically or by cuisine if helpful.
- Place a small bin or tray to collect recyclables.
- Keep a fire-safe area around the stove.
- Take a short stretch break while waiting for water to boil.
- Use timers to remind you to check on baking items.
- Keep an apron hanging near the kitchen entrance.
- Designate a drawer for reusable cutlery for lunches.
- Store cutting boards away from sources of moisture.
- Place herbs in jars with water like small bouquets.
- Keep a few “one pan” recipes visible on the fridge.
- Use stable step mats to avoid slipping near the sink.
- Store heavier items lower for safety.
- Keep light items like herbs and spices higher.
- Pre-measure spices for recipes into small bowls.
- Use chilled bowls for salads in warmer months.
- Keep a dedicated space for a slow cooker or rice cooker.
- Store recipe books or printouts in a dry space.
- Take a picture of recipes you like for quick recall.
- Keep pens near the recipe area for small tweaks.
- Note down what worked well after trying a new recipe.
- Store lunch boxes and bottles together in one cupboard.
- Keep reusable bags or totes by the door for grocery runs.
- Prioritise a clear walking path from fridge to stove.
- Use drawer organisers to separate utensils.
- Group baking trays together vertically.
- Store parchment paper and foil within easy reach.
- Lay a cloth under cutting boards if they slip.
- Place sharp tools out of reach of small children.
- Keep a safe place to cool hot dishes.
- Arrange surfaces so you can set down groceries quickly.
- Assign a zone for unpacking and washing produce.
- Keep a simple salad spinner if you enjoy leafy greens.
- Store nuts and seeds in airtight containers.
- Place frequently used cereals or grains at eye level.
- Try to keep a clutter-free corner for plating and photos.
- Keep a small jar of tasting spoons for sauces and soups.
- Use clear bins to group snacks in the pantry.
- Rotate through herbs and spice blends to avoid boredom.
- Keep a list of “use me first” items in the fridge.
- Designate nights for “clear the fridge” meals.
- Save jars for storing leftovers or dressings where appropriate.
- Ensure good airflow in the fridge by avoiding overcrowding.
- Check fridge temperatures for food safety.
- Place a small container of baking soda to reduce odours.
- Use fridge door space for condiments rather than milk.
- Group plant-based proteins in a clear fridge bin.
- Keep cooking oils away from direct sunlight.
- Store potatoes and onions in a cool, dark place.
- Keep a small basket for fresh bread or wraps.
- Wipe cupboard handles regularly for hygiene.
- Allocate a tiny drawer or box for measuring tools.
- Keep extra dish towels within reach of splash zones.
- Place cutting boards upright to dry after washing.
- Ensure that knives are completely dry before storing.
- Use sturdy, heat-proof utensils when cooking.
- Keep a spare set of tongs near the stove.
- Hang a calendar where you can pencil in meal plans.
- Keep coupons or store loyalty cards near grocery bags.
- Use stackable containers to maximise fridge space.
- Store meats on the lowest shelf in leak-proof containers.
- Group dairy products together away from the fridge door.
- Keep a gentle all-purpose spray for wiping counters.
- Wipe cutting boards immediately after use.
- Rinse sink basins after emptying pots or pans.
- Use drying racks that allow good airflow around dishes.
- Rotate dish cloths and sponges for freshness.
- Let pots and pans dry fully before stacking.
- Store kitchen appliances that you use rarely in higher cupboards.
- Place frequently used appliances like blenders at counter level.
- Maintain a safe, clutter-free area around electrical sockets.
- Keep cords organised and away from hot elements.
- Unplug small appliances when not in use.
- Make room for a comfortable standing position while cooking.
- Consider a small kitchen mat to reduce fatigue.
- Keep the floor clear of boxes and bags.
- Create a basic checklist for pre-cooking setup.
- Take a slow breath before you begin prepping food.
- Put on music or a podcast that supports a calm mood.
- Adjust lighting or open curtains to invite natural light.
- Declutter one small area of the kitchen each week.
- Celebrate how these small changes support regular cooking.
"""

MINDFUL_EATING_REFLECTIONS = """
HealthyPath4Life — gentle reflections for meals and snacks

- Before eating, ask: What does my body need right now?
- Notice where you feel hunger in the body.
- Give your hunger a simple word: gentle, loud, steady, quiet.
- Ask if you are physically hungry, emotionally hungry, or both.
- Take a breath and name your current emotion without judging it.
- Consider what kind of meal would feel supportive in this moment.
- Observe smells, colours and textures before the first bite.
- Take the first bite slowly and really notice the taste.
- Check in on your hunger level after a few bites.
- Ask if the meal is matching what you were hoping for.
- Notice if you are rushing, and gently slow down if you can.
- Put utensils down briefly to pause between bites.
- Look away from screens for a few seconds while chewing.
- See if you can spot at least two colours on your plate.
- Appreciate the effort that brought this food to you.
- If you feel guilt, gently remind yourself that all foods fit.
- Ask: What do I enjoy about this meal?
- Ask: How is this meal helping my energy or mood?
- Notice the moment you first feel comfortable, not stuffed.
- Consider what the difference feels like between satisfied and overly full.
- If you pass comfortable fullness, note it kindly for next time.
- Reflect on whether the environment is helping you enjoy the meal.
- Ask if a change in lighting, noise or posture might help.
- Consider standing to stretch for a moment mid-meal.
- Tune into how your jaw and shoulders feel while chewing.
- If you are multitasking, see if you can focus on one thing.
- Explore how different meal speeds feel in your body.
- Notice which meals lead to long-lasting energy.
- Notice which meals leave you hungry again quickly.
- Reflect on whether protein, fibre and fats were present.
- Consider what you might add rather than what you would remove.
- After a meal, ask if you feel alert, sleepy or neutral.
- Observe whether some foods affect your sleep.
- Gently track how late meals influence your digestion.
- Notice if caffeine changes your hunger or fullness signals.
- Make space for comfort foods without labelling them.
- After eating a comfort meal, observe comfort in the body.
- Ask what else might support you emotionally besides food.
- Keep a short list of non-food comforts on your phone.
- Reflect on the company you keep during meals.
- Ask if particular people or settings help you eat mindfully.
- Consider simple changes if certain patterns feel unhelpful.
- Celebrate any instance of slowing down or checking in.
- Acknowledge that distraction is normal in busy lives.
- Consider taking a few breaths after finishing the meal.
- Ask how this meal aligns with your overall intentions.
- Reflect on what worked well about this meal.
- Reflect on anything you might tweak next time.
- Capture learnings in a gentle note, not a strict rule.
- If the meal felt unsatisfying, ask what was missing.
- If the meal felt wonderful, note what supported that.
- Compare experiences of different breakfast types.
- Compare how you feel after various snacks.
- Notice which snacks sustain you between meals.
- Explore how adding fruit or vegetables changes things.
- Try pairing carbohydrates with protein or fat and observe.
- Reflect on drinking water before, during or after meals.
- Notice whether eating in silence feels calming or stressful.
- Alternate between mindful bites and conversation when socialising.
- Ask how your body feels before and after social meals.
- Reflect on the stories you have learned about certain foods.
- Consider which stories still serve you and which do not.
- Practice speaking kindly to yourself about food choices.
- Notice when perfectionism appears in your thoughts.
- Remind yourself that patterns matter more than single meals.
- Let go of the idea of “starting over” with every slip.
- Acknowledge that appetite ebbs and flows day to day.
- Observe how stress shifts your hunger or cravings.
- Gently experiment with strategies that ease stress.
- Reflect on how sleep quality affects hunger.
- Consider how movement influences your appetite.
- Note any patterns between heavy meals and energy dips.
- Observe how lighter meals feel in contrast.
- Pay attention to how cultural foods fit into your patterns.
- Celebrate meals that connect you to your culture or family.
- Make room for flexibility around special occasions.
- Reflect on what felt joyful about a celebration meal.
- Ask how you might support your body after rich meals.
- Notice when you skip meals and how that feels later.
- Experiment with more regular eating if that feels better.
- Reflect on how long gaps impact mood and focus.
- Explore whether gentle snacks help stabilise your day.
- Track simple cues like irritability or fatigue.
- Ask which meals help you feel grounded and steady.
- Keep a note of meals that feel too heavy at certain times.
- Adjust portion sizes when you have new information.
- Recognise that needs change across seasons of life.
- Reflect on any all-or-nothing thoughts that appear.
- Gently replace them with more flexible phrases.
- Invite curiosity instead of criticism into your reflections.
- Consider what future-you would thank you for.
- Acknowledge that some days mindful eating is easier.
- Trust that practice gradually builds familiarity.
- Use v3gn logs as a mirror, not a scorecard.
- Notice which path tags feel most aligned with your goals.
- Experiment with new paths gently and track how they feel.
- Use reflections to adjust your goals over time.
- Honour your body’s cues alongside your values and context.
- Remind yourself that you deserve adequate, enjoyable food.
- Recognise that every meal is an opportunity to learn.
"""

MEAL_PLANNING_SCENARIOS = """
HealthyPath4Life — simple planning scenarios to explore

- Plan a “no-recipe” week using only simple templates.
- Choose three breakfasts you can rotate easily.
- Choose three lunches that pack well for work or school.
- Choose three dinners you can make in under 30 minutes.
- Build a grocery list directly from those nine ideas.
- Plan one plant-focused dinner each week to try new meals.
- Plan one high-protein breakfast that feels gentle on digestion.
- Add one “clear-the-fridge” meal to every week.
- Include at least one soup or stew for flexible leftovers.
- Plan a grain bowl night with mix-and-match toppings.
- Plan a wrap night with vegetables, spreads and proteins.
- Schedule one slow-cooker or pressure-cooker meal.
- Include one meal that uses mostly pantry items.
- Plan one comfort meal that supports emotional ease.
- Identify which nights usually feel busiest.
- Assign your simplest meals to the busiest nights.
- Assign more involved recipes to flexible evenings.
- Keep one backup frozen meal for unexpected days.
- Plan a “picnic-style” dinner with easy components.
- Include snacks in your weekly planning, not just meals.
- Check existing pantry items before writing a list.
- Use v3gn to note ideas under suitable path tags.
- Create a shortlist of meals everyone in the home enjoys.
- Label a few meals as “weeknight heroes”.
- Plan to batch cook a grain at the start of the week.
- Plan to batch cook a protein like beans or chicken pieces.
- Plan to wash and chop vegetables once for multiple uses.
- Consider which meals can share ingredients (e.g. rice, beans).
- Group recipes that use similar fresh items to reduce waste.
- Plan bowls that use leftover roast vegetables.
- Plan salads that use leftover cooked grains.
- Plan wraps using leftover proteins and vegetables.
- Plan omelettes or frittatas to use small amounts of veg.
- Write down at least one very simple backup breakfast.
- Write down at least one very simple backup lunch.
- Write down at least one very simple backup dinner.
- Identify meals that can be assembled without cooking.
- Note which ingredients can move between meals if plans change.
- Assign one evening to check supplies and adjust.
- Keep planning sessions short and light-hearted.
- Involve other household members in choosing meals.
- Let each person choose one meal for the week.
- Keep a running list of meals that worked well.
- Highlight meals that reheat particularly well.
- Note any meals that were too complex for this season.
- Adjust recipes to better match your energy and skills.
- Plan themed nights like “grain bowl Tuesday” if fun.
- Rotate themes when you get bored of current ones.
- Check your calendar for late finishes and plan accordingly.
- Plan portable meals for evenings out or long days.
- Think about how leftovers will be stored and labelled.
- Check container availability before batch cooking.
- Plan ahead for travel days with simpler options.
- Include one meal that uses up herbs or greens.
- Include one meal that uses up root vegetables.
- Check which condiments or sauces are running low.
- Refill staples like oil, spices or grains as needed.
- Look ahead to any celebrations or guests.
- Plan meals that can stretch easily with extra sides.
- Keep breakfast ingredients flexible for different appetites.
- Make room for spontaneous meals out when it feels right.
- Allow a buffer night for leftovers or simple toast-and-eggs.
- Plan multiple uses for perishable items like fresh berries.
- Consider seasonality when choosing produce-heavy meals.
- Swap in frozen produce if fresh options are limited.
- Plan shelf-stable snacks for backup support.
- Store planning notes where you will actually see them.
- Use digital tools or paper, whichever you prefer.
- Revisit plans mid-week and shift meals as needed.
- Note any patterns: which meals often get skipped.
- Adjust portion sizes of recipes for your household size.
