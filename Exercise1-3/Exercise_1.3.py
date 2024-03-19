recipes_list = []

ingredients_list = []

def take_recipes():
    name = input("Enter recipe name: ")
    cooking_time = int(input("Enter cooking times in minutes: "))
    ingredients = input("Enter recipe Ingredients: ").split(", ")
    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients
    }
    return recipe

n = int(input("How many recipes would you like to enter?: "))

for i in range(n):
    recipe = take_recipes()
    for ingredient in recipe["ingredients"]:
        if not ingredient in ingredients_list:
            ingredients_list.append(ingredient)
    recipes_list.append(recipe)

for recipe in recipes_list:
    if recipe["cooking_time"] < 10 and len(recipe["ingredients"]) < 4:
        recipe["difficulty"] = "Easy"
    elif recipe["cooking_time"] < 10 and len(recipe["ingredients"]) >= 4:
        recipe["difficulty"] = "Medium"
    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) < 4:
        recipe["difficulty"] = "Intermediate"
    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) >= 4:
        recipe["difficulty"] = "Hard"

for recipe in recipes_list:
    print("Recipe: ", recipe["name"])
    print("Cooking time (in miuntes): ", recipe["cooking_time"])
    print("Ingredients: ")
    for ingredient in recipe["ingredients"]:
        print(ingredient)
    print("Difficulty: ", recipe["difficulty"])

def alpha_ingredients():
    ingredients_list.sort()
    print("Ingredients Available In All Recipes")
    print("____________________________________")
    for ingredient in ingredients_list:
        print(ingredient)

alpha_ingredients()
