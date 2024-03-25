import pickle

def display_recipe(recipes):
    if len(recipes) > 0:
        first_recipe = recipes[0]
        print("Recipe: " + first_recipe["name"])
        print("Cooking Time: " + str(first_recipe["cooking_time"]))
        print("Ingredients: " + ", ".join(first_recipe["ingredients"]))
        print("Difficulty: " + first_recipe["difficulty"])
    else:
        print("No recipe to display.")


def search_ingredient(data):
    print("Available Ingredients:")
    for index, ingredient in enumerate(data["Ingredients list"], start=1):
        print(str(index) + ". " + ingredient)
    try:
        list_number = int(input("Please pick a number: ")) - 1
        ingredient_searched = list_number
    except:
        print("Incorrect input entered.")
    else:
        ingredients_list = data["Ingredients list"]
    if 0 <= list_number < len(ingredients_list):
        ingredient_searched = ingredients_list[list_number]
        for recipe in data["Recipes list"]:
            if ingredient_searched in recipe["ingredients"]:
                print("Recipe: " + recipe["name"])
                print("Cooking Time: " + str(recipe["cooking_time"]))
                print("Ingredients: " + ", ".join(recipe["ingredients"]))
                print("Difficulty: " + recipe["difficulty"])
    else:
        print("Please chose a number thats listed!")


recipe_file_name = str(input("Please enter the file name containing your recipe or recipes: "))

try:
    recipes_file = open(recipe_file_name + ".bin", "rb")
    data = pickle.load(recipes_file)
except FileNotFoundError:
    print("File cannot be found, please try again.")
else:
    search_ingredient(data)