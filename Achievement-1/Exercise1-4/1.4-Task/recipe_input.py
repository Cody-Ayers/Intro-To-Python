import pickle

recipe_list = []
ingredient_list = []


def calc_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        difficulty = "easy"
        return difficulty
    elif cooking_time < 10 and len(ingredients) >= 4:
        difficulty = "medium"
        return difficulty
    elif cooking_time >= 10 and len(ingredients) < 4:
        difficulty = "intermediate"
        return difficulty
    elif cooking_time >= 10 and len(ingredients) >= 4:
        difficulty = "hard"
        return difficulty


def take_recipe():
    name = str(input("Please enter the recipe name: "))
    cooking_time = int(input("Please enter the cooking time in minutes: "))
    ingredients_input = str(
        input(
            "Please enter the list of ingredients: "))
    ingredients = ingredients_input.split(", ")
    difficulty = calc_difficulty(cooking_time, ingredients)
    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients,
        "difficulty": difficulty,
    }
    return recipe


recipe_file_name = (str(input("Enter the filename for which you would like to store your recipe(s): ")) + ".bin")

try:
    recipes_file = open(recipe_file_name, "rb")
    data = pickle.load(recipes_file)
except FileNotFoundError:
    print("File name not found.")
    data = {"Recipes list": recipe_list, "Ingredients list": ingredient_list}
except:
    print("Unexpected errors have occurred.")
    data = {"Recipes list": recipe_list, "Ingredients list": ingredient_list}
else:
    recipes_file.close()
finally:
    recipes_list = data["Recipes list"]
    print("This file already contains the following recipes: " + str(recipes_list))
    ingredients_list = data["Ingredients list"]
    print("and this list of ingredients: " + str(ingredients_list))

recipes_number = int(input("Enter how many recipe(s) you would like to create: "))
n = recipes_number

for number_recipe_specified in range(n):
    recipe = take_recipe()
    recipe_list.append(recipe)
    for ingredient in recipe["ingredients"]:
        if not ingredient in ingredient_list:
            ingredient_list.append(ingredient)

print("This is the updated recipe file, with the new added recipe(s): " + str(data))

recipes_file = open(recipe_file_name, "wb")
pickle.dump(data, recipes_file)
recipes_file.close()