import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='cf-python',
    passwd='password'
)

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

cursor.execute("USE task_database")

cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
    id              INT PRIMARY KEY AUTO_INCREMENT,
    name            VARCHAR(50),
    ingredients     VARCHAR(255),
    cooking_time    INT,
    difficulty      VARCHAR(20)
)''')

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

def create_recipe(conn, cursor):
    try:
        name = str(input("Please enter the recipe name: "))
        cooking_time = int(input("Please enter the cooking time in minutes: "))
        ingredients_input = str(input("Please enter the list of ingredients separated by a comma: "))
        ingredients = ingredients_input.split(", ")
        difficulty = calc_difficulty(cooking_time, ingredients)

        sql = "INSERT INTO Recipes (name, cooking_time, ingredients, difficulty) VALUES (%s, %s, %s, %s)"
        val = (name, cooking_time, ", ".join(ingredients), difficulty)
        cursor.execute(sql, val)
        conn.commit()

        print("~~__~~__~~__~~__~~__~~__~~")
        print("Recipe successfully added!")
        print("~~__~~__~~__~~__~~__~~__~~")

    except:
        print("An Error has occurred while entering your recipe")
        


def search_recipe(conn, cursor):
    all_ingredients = []

    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()

    for ingredients in results:
        ingredients_string = ingredients[0]
        ingredients = ingredients_string.split(", ")

        for item in ingredients:
            if item not in all_ingredients:
                all_ingredients.append(item)

    print("Use this list of ingredients to search for recipes.")
    print("~~__~~__~~__~~__~~__~~__~~__~~__~~__~~__~~__~~__~~")
    print()

    for index, ingredient in enumerate(all_ingredients, start=1):
        print(str(index) + ". " + ingredient)

    search_ingredient = None

    try:
        print("~~__~~__~~__~~__~~__~~__~~__~~__")
        number_from_list = int(input("Pick a number from the list: ")) - 1
        search_ingredient = all_ingredients[number_from_list]
        print("~~__~~__~~__~~__~~__~~__~~__~~__")
        print("Ingredient Selected: " + search_ingredient)
        print("~~__~~__~~__~~__~~__~~__~~__~~__")

        sql = "SELECT name, cooking_time, ingredients, difficulty FROM Recipes WHERE ingredients LIKE %s"
        val = ("%" + search_ingredient + "%",)
        cursor.execute(sql, val)
        result = cursor.fetchall()
        print("Here are the recipe(s) containing this ingredient:")
        for row in result:
            print("Name: ", row[0])
            print("Cooking Time: ", row[1])
            print("Ingredients: ", row[2])
            print("Difficulty: ", row[3])

    except:
        print("Please choose a number from the list")

def update_recipe(conn, cursor):

    cursor.execute("SELECT id, name, cooking_time, ingredients, difficulty FROM Recipes")

    print("~~__~~__~~__~~__~~__~~__~~__~~__~~__~~__")
    print("These is all the recipes you can update:")
    print()

    result = cursor.fetchall()
    for row in result:
        print("Recipe number: ", row[0]) 
        print("Name: ", row[1])
        print("Cooking Time: ", row[2])
        print("Ingredients: ", row[3])
        print("Difficulty:", row[4])
        print()

    try:
        print("~~__~~__~~__~~__~~__~~__~~__~~__~~__~~")
        recipe_selected = int(input("Choose recipe to update based on its number: "))
        print("~~__~~__~~__~~__~~__~~__~~__~~__~~__~~")
        print("Items that you can choose to update: ")
        print()
        print("1. Name")
        print("2. Cooking Time")
        print("3. Ingredients")
        field_selected = int(input("Enter the item number for which you want to update: "))

        if field_selected == 1:
            updated_name = str(input("Please enter the new recipe name: "))

            sql = "UPDATE Recipes SET name = %s WHERE id=%s"
            val = (updated_name, recipe_selected)
            cursor.execute(sql, val)
            conn.commit()

            print("~~__~~__~~__~~__~~__~~__~~__~~__~~")
            print("Name successfully updated!")

        if field_selected == 2:
            cursor.execute("SELECT ingredients FROM Recipes WHERE id = %s", (recipe_selected,))
            results = cursor.fetchall()
            ingredients_string = results[0][0]
            ingredients = ingredients_string.split(", ")

            updated_cooking_time = int(input("Enter the new cooking time (in min) for this recipe: "))
            updated_difficulty = calc_difficulty(updated_cooking_time, ingredients)

            sql_cooking_time = "UPDATE Recipes SET cooking_time = %s WHERE id=%s"
            val_cooking_time = (updated_cooking_time, recipe_selected)
            cursor.execute(sql_cooking_time, val_cooking_time)

            sql_difficulty = "UPDATE Recipes SET difficulty = %s WHERE id=%s"
            val_difficulty = (updated_difficulty, recipe_selected)
            cursor.execute(sql_difficulty, val_difficulty)

            conn.commit()

            print("~~__~~__~~__~~__~~__~~__~~__~~__~~")
            print("Cooking Time successfully updated!")

        if field_selected == 3:
            cursor.execute("SELECT cooking_time FROM Recipes WHERE id = %s", (recipe_selected,))
            results = cursor.fetchall()
            cooking_time = results[0][0]

            ingredients_input = str(input("Please enter the new list of ingredients: "))
            updated_ingredients = ingredients_input.split(", ")
            updated_difficulty = calc_difficulty(cooking_time, updated_ingredients)

            sql_ingredients = "UPDATE Recipes SET ingredients = %s WHERE id=%s"
            val_ingredients = (", ".join(updated_ingredients), recipe_selected)
            cursor.execute(sql_ingredients, val_ingredients)

            sql_difficulty = "UPDATE Recipes SET difficulty = %s WHERE id=%s"
            val_difficulty = (updated_difficulty, recipe_selected)
            cursor.execute(sql_difficulty, val_difficulty)

            conn.commit()

            print("~~__~~__~~__~~__~~__~~__~~__~~__~~")
            print("Ingredients successfully updated!")

    except:
        print("Please choose a number from the list")

def delete_recipe(conn, cursor):
    cursor.execute("SELECT id, name, ingredients, cooking_time, difficulty FROM Recipes")

    print("~~__~~__~~__~~__~~__~~__~~__~~__~~__~~__~~__~~")
    print("Choose which recipe you would like to delete:")
    print()

    result = cursor.fetchall()

    for row in result:
        print("Recipe number: ", row[0]) 
        print("Name: ", row[1])
        print("Cooking Time: ", row[2])
        print("Ingredients: ", row[3])
        print("Difficulty:", row[4])
        print()

    try:
        print("~~__~~__~~__~~__~~__~~__~~__~~__~~__~~")
        recipe_selected = int(input("Choose a recipe to delete by selecting its number: "))

        sql = "DELETE FROM Recipes WHERE id=%s"
        val = (recipe_selected,)
        cursor.execute(sql, val)
        conn.commit()

        print("You have successfully deleted the recipe!")

    except:
        print("Please choose a number from the list")


def main_menu(conn, cursor):

    user_choice = None

    while user_choice != "quit":
        print("~~__~~---~~__~~ Main Menu ~~__~~---~~__~~")
        print("~~__~~__~~__~~__~~__~~__~~__~~__~~__~~__~~")
        print("~~__~~ Select an option from below ~~__~~")
        print("1. Create a New Recipe")
        print("2. Search for a Recipe by Ingredients")
        print("3. Update a Recipe")
        print("4. Delete a Recipe")
        print('Type "quit" to exit')

        user_choice = input("Please pick a number or (type 'quit' to exit): ")

        if user_choice == "1":
            create_recipe(conn, cursor)
            continue
        elif user_choice == "2":
            search_recipe(conn, cursor)
            continue
        elif user_choice == "3":
            update_recipe(conn, cursor)
            continue
        elif user_choice == "4":
            delete_recipe(conn, cursor)
            continue
        elif user_choice == "quit":
            conn.commit()
            conn.close()
            break

    print("You chose: " + str(user_choice))


main_menu(conn, cursor)