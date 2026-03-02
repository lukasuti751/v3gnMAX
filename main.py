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
