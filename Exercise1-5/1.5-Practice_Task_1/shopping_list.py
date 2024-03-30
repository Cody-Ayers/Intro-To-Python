class ShoppingList(object):
    # Create list method
    def __init__(self, list_name):
        self.list_name = list_name
        self.shopping_list = []

    # Add an item method
    def add_item(self, item):
        if item not in self.shopping_list:
            self.shopping_list.append(item)
        else:
            print("Sorry, " + item + " is already on the shopping list and cannot be added.")

    # Remove an item method
    def remove_item(self, item):
        if item in self.shopping_list:
            self.shopping_list.remove(item)

    # Method used to view the list
    def view_list(self):
        print(self.list_name + " has the following items listed")
        for item in self.shopping_list:
            print(item)


# Create pet store list object
pet_store_list = ShoppingList("Pet Store List")

# Add items to pet store list using add_item method
pet_store_list.add_item("dog food")
pet_store_list.add_item("frisbee")
pet_store_list.add_item("bowl")
pet_store_list.add_item("collars")
pet_store_list.add_item("flea collars")

# Removing an item from the list using remove_item method
pet_store_list.remove_item("flea collars")

# Test to check code on adding an item already on the list
pet_store_list.add_item("frisbee")

# Using the view_list method to print the list
pet_store_list.view_list()

