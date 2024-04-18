# Importing packages and methods to build Recipe Application 
from sqlalchemy import create_engine

engine = create_engine("mysql://cf-python:password@localhost/task_database")

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

from sqlalchemy import Column
from sqlalchemy.types import Integer, String

# Defining the Recipe Model
class Recipe(Base):
    # Define table and columns
    __tablename__ = "final_recipes"
    
    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))
    
   
    def __repr__(self):
        return "Recipe ID: " + str(self.id) + ", Name: " + self.name + ", Difficulty: " + self.difficulty
    
    # Printing well-formatted recipes
    def __str__(self):
        recipe = "\nRecipe ID: " + str(self.id)
        recipe += "\nRecipe Name: " + self.name
        recipe += "\nCooking Time: " + str(self.cooking_time)
        recipe += "\nIngredients: "
        for ingredient in self.return_ingredients_as_list():
            recipe += "\n\t" + ingredient
        recipe += "\nDifficulty: " + self.difficulty

        return recipe
    
    # Calculate the difficulty of a recipe based on the number of ingredients and cooking time
    def calculate_difficulty(self):
        num_of_ingredients = len(self.return_ingredients_as_list())

        if self.cooking_time < 10 and num_of_ingredients < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and num_of_ingredients >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and num_of_ingredients < 4:
            self.difficulty = "Intermediate"
        elif self.cooking_time >= 10 and num_of_ingredients >= 4:
            self.difficulty = "Hard"

    def return_ingredients_as_list(self):
        if self.ingredients == "": return []
        return self.ingredients.split(", ")

Base.metadata.create_all(engine)

# Create a new recipe
def create_recipe():

    # Allow user to enter recipe name
    while True:
        name = str(input("Enter the name of your recipe: "))
        if len(name) > 50:
            print("Recipe name must not exceed 50 characters. Please change your recipe name. ")
        else: break

    # Allow user to enter cooking time
    while True:
        cooking_time = input("Enter cooking time in minutes: ")
        if not cooking_time.isnumeric():
            print("~~__~~" * 8 + "\n")
            print("Only numbers can be used for cooking time. Update cooking time with a number. ")
            print("~~__~~" * 8)
        else:
            cooking_time = int(cooking_time)
            break

    # Allow user to enter recipe ingredients
    ingredients_list = []
    while True:
        ingredient = str(input("Please enter an ingredient, when done hit enter: "))
        if ingredient != "":
            ingredients_list.append(ingredient)
        else: break
    ingredients = ", ".join(ingredients_list)

    recipe_entry = Recipe(name=name, ingredients=ingredients, cooking_time=cooking_time)
    recipe_entry.calculate_difficulty()

    # Committing recipe to the database
    session.add(recipe_entry)
    session.commit()

# View all recipes
def view_all_recipes():
    all_recipes = session.query(Recipe).all()
    if len(all_recipes) < 1:
        print("There are currently no recipes in the database. Redirecting you back to Main Menu.")
        return
    for recipe in all_recipes:
        print(recipe)

# Search by ingredients
def search_by_ingredients():
    # Check to make sure recipes exist
    if session.query(Recipe).count() < 1:
        print("There are currently no recipes in the database. Redirecting you back to Main Menu.")
        return
    
    # Retrieve recipes from the database
    results = session.query(Recipe.ingredients).all()
    all_ingredients = []

    # Create a list of every ingredient, without listing multiples
    for str in results:
        ingredient_list = str[0].split(", ")
        for ingredient in ingredient_list:
            if not ingredient in all_ingredients:
                all_ingredients.append(ingredient)

    # Print all ingredients
    for count, ingredient in enumerate(all_ingredients):
        print(count, ingredient)

    # User gets to select ingredients and also check that value is valid
    ingredients_input = input("Enter the number or numbers of the ingredients that you would like to search for recipes with. \n If you want to search with more that one ingredient, separate numbers by only a space. \n Number(s) chosen: ")
    items = ingredients_input.split(" ")
    search_ingredients = []
    for itm in items:
        if not itm.isnumeric():
            print("Input is not a number")
            return
        else: itm = int(itm)
        if itm < 0 or itm >= len(all_ingredients):
            print("Input length is too long")
            return
        
        # Create searched ingredients list
        search_ingredients.append(all_ingredients[int(itm)])

    # Search for recipes that with ingredients that user selected
    conditions = []
    for search_ingredient in search_ingredients:
        like_term = "%" + search_ingredient + "%"
        conditions.append(Recipe.ingredients.like(like_term))
    recipes = session.query(Recipe).filter(*conditions).all()

    # Print all resulting recipes
    for recipe in recipes:
        print(recipe)

# Edit recipes
def edit_recipe():
    # Check to make sure recipes exist
    if session.query(Recipe).count() < 1:
        print("There are currently no recipes in the database. Redirecting you back to Main Menu.")
        return
    
    # Retrieve id and name from each recipe in database to store in results
    results = session.query(Recipe).with_entities(Recipe.id, Recipe.name).all()

    # Display recipes available to the user to choose from
    ids = []
    for recipe in results:
        print(recipe[0], recipe[1])
        ids.append(recipe[0])

    # Get ID of recipe from user
    try:
        id = int(input("Please enter the id of the recipe that you'd like to edit, then hit enter: "))
    except:
        print("Input in invalid, returning to the Main Menu.")
        return
    
    # Making sure that ID is valid
    if not id in ids:
        print("ID not found! Going back to main menu.")
        return
    
    # Display what is editable to the user
    recipe_to_edit = session.query(Recipe).filter(Recipe.id == id).one()
    print("1 ~ Name: ", recipe_to_edit.name)
    print("2 ~ Ingredients: ", recipe_to_edit.ingredients)
    print("3 ~ Cooking Time: ", recipe_to_edit.cooking_time)

    # User selects what to edit
    try:
        num = int(input("Choose which you'd like to edit by selecting its number: "))
    except:
        print("Invalid input, returning to Main Menu.")
        return
    
    # Edit Name
    if num == 1:
        while True:
            name = str(input("Enter the new name for your recipe: "))
            if len(name) > 50:
                print("Recipe name must not exceed 50 characters. Please change your recipe name. ")
            else: break
        recipe_to_edit.name = name

    # Edit ingredients
    elif num == 2:
        ingredients_list = []
        while True:
            ingredient = str(input("Please enter an ingredient, when done hit enter: "))
            if ingredient != "":
                ingredients_list.append(ingredient)
            else: break
        ingredients = ", ".join(ingredients_list)
        recipe_to_edit.ingredients = ingredients
        recipe_to_edit.calculate_difficulty()

    # Edit Cooking Time
    elif num == 3:
        while True:
            cooking_time_input = input("Enter the new cooking time for your recipe: ")
            if not cooking_time_input.isnumeric():
                print("Only numbers can be used for cooking time. Update cooking time with a number. ")
            else:
                cooking_time = int(cooking_time_input)
                break
        recipe_to_edit.cooking_time = cooking_time
        recipe_to_edit.calculate_difficulty()
    else:
        print("Invalid number, returning to Main Menu.")
        return
    
    # Commit changes
    session.commit()

# Delete recipes
def delete_recipe():

    # Check to make sure recipes exist
    if session.query(Recipe).count() < 1:
        print("There are currently no recipes in the database. Redirecting you back to Main Menu.")
        return
    
    # Get recipe names and ids from the database
    results = session.query(Recipe).with_entities(Recipe.id, Recipe.name).all()

    # Display all recipes to user based on recipe id
    ids = []
    for recipe in results:
        print(recipe[0], recipe[1])
        ids.append(recipe[0])

    # Allow user to chose recipe to delete based on id
    try:
        id = int(input("Please choose which recipe to delete by entering its ID then hitting enter: "))
    except:
        print("Invalid input, returning to Main Menu.")
        return
    
    # Check to make sure the ID is valid
    if not id in ids:
        print("ID entered is not found, returning to Main Menu.")
        return
    recipe_to_delete = session.query(Recipe).filter(Recipe.id == id).one()
    print(recipe_to_delete)
    
    choice = input("Continue to delete this recipe? type ' yes ' and hit enter to continue: ")
    if choice == "yes":
        session.delete(recipe_to_delete)
        session.commit()
        print("Recipe has been deleted")


user_choice = ""
while (user_choice != "quit"):
    print("<~~--~~--~~--~~--~~--~~--~~--~~--~~--~~--~~--~~>")
    print("<><><><><>          Main menu         <><><><><>")
    print("<~~--~~--~~--~~--~~--~~--~~--~~--~~--~~--~~--~~>")
    print("<><><><><>        Pick a choice       <><><><><>")
    print("<~~--~~--~~--~~--~~--~~--~~--~~--~~--~~--~~--~~>" + "\n")
    print("< 1 >           Create New Recipe          < 1 >")
    print("< 2 >           View all recipes           < 2 >")
    print("< 3 >  Search for a recipe by ingredients  < 3 >")
    print("< 4 >             Edit a recipe            < 4 >")
    print("< 5 >            Delete a recipe           < 5 >")
    print("<><><><><>     Type 'quit' to exit    <><><><><>")
    user_choice = input("Choose a number or type 'quit' to exit: ")

    if user_choice == "1": create_recipe()
    elif user_choice == "2": view_all_recipes()
    elif user_choice == "3": search_by_ingredients()
    elif user_choice == "4": edit_recipe()
    elif user_choice == "5": delete_recipe()
    elif user_choice != "quit": print("Invalid input!")

# End: Closing session and database
session.close()
engine.dispose()