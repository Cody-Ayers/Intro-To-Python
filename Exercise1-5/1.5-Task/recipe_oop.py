# Recipe Class defined
class Recipe(object):
    ingredients_list = []

    def __init__(self, name):
        self.name = name
        self.cooking_time = int(0)
        self.ingredients = []
        self.difficulty = ""

    #  Method to determine cooking difficulty
    def calc_difficulty(self, cooking_time, ingredients):
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
    
    # Getter method for recipe name
    def get_name(self):
        output = "Recipe Name: " +str(self.name)
        return output
    
    # Setter method for recipe
    def set_name(self, name):
        self.name = name

    # Getter method for cooking time
    def get_cooking_time(self):
        output = "Cooking time (minutes): " + str(self.cooking_time)
        return output
    
    # Setter method for cooking time
    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time
        self.difficulty = self.calc_difficulty(self.cooking_time, self.ingredients)

    # Update to add ingredients
    def add_ingredients(self, *ingredients):
        for ingredient in ingredients:
            if ingredient not in self.ingredients:
                self.ingredients.append(ingredient)
                self.update_all_ingredients()
                self.difficulty = self.calc_difficulty(self.cooking_time, self.ingredients)
            else:
                print("When trying to add " + str(ingredient) + " to the recipe list, we found that ingredient already exists.")

    # Getter method for ingredients
    def get_ingredients(self):
        output = self.ingredients
        return output
    
    # Getter method for difficulty
    def get_difficulty(self):
        if self.difficulty == "":
            self.difficulty = self.calc_difficulty(self.cooking_time, self.ingredients)
            output = "Difficulty level: " + self.difficulty
            return output
        else:
            output = "Difficulty level: " + self.difficulty
            return output

    # Search ingredient method
    def search_ingredient(self, ingredients_searched):
        for ingredients in self.ingredients:
            if ingredients == ingredients_searched:
                return True
        else:
            return False

    # Update Ingredients List method        
    def update_all_ingredients(self):
        for ingredients in self.ingredients:
            if not ingredients in Recipe.ingredients_list:
                Recipe.ingredients_list.append(ingredients)

    # Method to define the output string        
    def __str__(self):
        output = (
            "Recipe Name: "
            + str(self.name)
            + "\nCooking Time (minutes): "
            + str(self.cooking_time)
            + "\nIngredients: "
            + str(self.ingredients)
            + "\nDifficulty Level: "
            + str(self.difficulty)
        )
        return output
    
    # Method for searching for a recipe
    def recipe_search(data, search_term):
        if not isinstance(data, list):
            data = [data]
        for recipe in data:
            if recipe.search_ingredient(search_term) is True:
                print(recipe)


# Main Code
                
# Adding objects
                
recipe_list = []

tea = Recipe("Tea")
tea.set_cooking_time(5)
tea.add_ingredients("Tea Leaves", "Sugar", "Water", "Salt")
tea.get_difficulty()
recipe_list.append(tea)

coffee = Recipe("Coffee")
coffee.set_cooking_time(5)
coffee.add_ingredients("Coffee Powder", "Sugar", "Water")
coffee.get_difficulty()
recipe_list.append(coffee)

cake = Recipe("Cake")
cake.set_cooking_time(50)
cake.add_ingredients("Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk")
cake.get_difficulty()
recipe_list.append(cake)

BananaSmoothie = Recipe("Banana Smoothie")
BananaSmoothie.set_cooking_time(5)
BananaSmoothie.add_ingredients("Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes")
BananaSmoothie.get_difficulty()
recipe_list.append(BananaSmoothie)


# Search for recipes that contain Water, Sugar and Bananas

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("The following Recipes contain 'Water': ")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
Recipe.recipe_search(recipe_list, "Water")


print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("The following Recipes contain 'Sugar': ")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
Recipe.recipe_search(recipe_list, "Sugar")



print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("The following Recipes contain 'Bananas': ")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
Recipe.recipe_search(recipe_list, "Bananas")



    
    


    