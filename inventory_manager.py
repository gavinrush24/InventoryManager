"""An command line inventory manager created for CPS 310.

Author: Gavin Rush
Course: CPS 310
Project: Inventory Manager
"""

INVENTORY_FILE = "inventory.txt"

def display_menu():
    """Display the available InventoryManager menu options."""

    print("\nInventoryManager Menu")
    print("1. View Inventory")
    print("2. Add an item")
    print("3. Update an item quantity")
    print("4. Remove an item")
    print("5. Search inventory")
    print("6. View inventory summary")
    print("7. Exit")


def load_inventory(filename):
    """Read inventory.txt and return a list of item dictionaries.
 
    Each line looks like: Name|Category|Quantity
    If the file doesn't exist, an empty inventory is returned.
    """
    inventory = []
 
    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if not line:  # skip empty lines
                    continue
 
                name, category, quantity = line.split("|")
                item = {
                    "name": name.strip(),
                    "category": category.strip(),
                    "quantity": int(quantity.strip()),
                }
                inventory.append(item)
    except FileNotFoundError:
        return []  # start with an empty inventory instead of crashing
 
    return inventory

def save_inventory(inventory, filename):
    """Write the complete current inventory to the file, one item per line."""

    with open(filename, "w") as file:
        for item in inventory:
            file.write(f"{item['name']}|{item['category']}|{item['quantity']}\n")
            
def view_inventory(inventory):
    """Print the inventory as a numbered list starting at 1."""
    if not inventory:
        print("No inventory items found.")
        return
 
    print("Inventory:")
    for number, item in enumerate(inventory, start=1):
        print(f"{number}. {item['name']} | {item['category']} | Quantity: {item['quantity']}")

def add_item(inventory):
    """Prompt the user for an item and add it to the inventory list."""

    name = input("Enter item name: ").strip().lower()
    if not name:
        print("Name cannot be empty.")
        return
    if "|" in name:
        print("Name cannot contain '|'.")
        return
    if any(existing["name"].lower() == name for existing in inventory):
        print("Duplicate items are not allowed.")
        return

    category = input("Enter the category: ").strip().lower()
    if not category:
            print("A task cannot be empty.")
            return
    if "|" in category:
            print("Category cannot contain '|'.")
            return

    quantity = input("Enter the quantity: ").strip()
    if not quantity.isdigit():
            print("Quantity must be a nonnegative whole number.")
            return

    item = {
        "name": name.title(),
        "category": category.title(),
        "quantity": int(quantity)
    }

    inventory.append(item)
    print("Item added successfully.")

def update_quantity(inventory):
    """Let the user pick an item and change its quantity."""

    if not inventory:
        print("No inventory items found.")
        return False

    view_inventory(inventory)

    item_number = select_item_number(inventory)
    if item_number is None:
        return False

    new_quantity = input("Enter the new quantity: ").strip()
    try:
        new_quantity = int(new_quantity)
    except ValueError:
        print("Quantity must be a whole number.")
        return False

    if new_quantity < 0:
        print("Quantity cannot be negative.")
        return False

    item = inventory[item_number - 1]
    item["quantity"] = new_quantity
    print(f"{item['name']} quantity updated to {new_quantity}.")

    return True

def remove_item(inventory):
    """Prompt the user to select and remove an item.
    
        Return True when a item is removed and False otherwise.
        """
    
    if not inventory:
            print("No items are available to remove.")
            return False
    
    view_inventory(inventory)

    item_number = select_item_number(inventory)
    if item_number is None:
            return False

    removed_item = inventory.pop(item_number - 1)
    
    print(f"'{removed_item['name']}' has been removed.")
    
    return True

def search_inventory(inventory):
    """Prompt for part of an item name and display every matching item."""

    search_term = input("Enter part or all of an item name: ").strip().lower()
    if not search_term:
        print("Search term cannot be empty.")
        return

    matches = []
    for item in inventory:
        if search_term in item["name"].lower():
            matches.append(item)

    if not matches:
        print("No inventory items matched your search.")
        return

    print("Search results:")
    for number, item in enumerate(matches, start=1):
        print(f"{number}. {item['name']} | {item['category']} | Quantity: {item['quantity']}")

def display_summary(inventory):
    """Display a summary of the inventory including unique items, total quantity, and low stock items"""

    total_items = 0
    low_stock = 0
    categories = {}

    for item in inventory:

        total_items += item['quantity']

        if item['quantity'] <= 5:
            low_stock += 1

        category = item['category']
        categories[category] = categories.get(category, 0) + 1

    print("Inventory Summary")
    print(f"Unique items: {len(inventory)}")
    print(f"Total quantity: {total_items}")
    print(f"Low-stock items: {low_stock}")
    print("")
    print("Items by category: ")

    for category in categories:
        print(f"{category}: {categories[category]}")


def select_item_number(inventory):
    """Ask for an item number and return it, or None if the input is invalid."""

    selection = input("Please enter item number: ").strip()
    if not selection.isdigit():
        print("Please enter a valid item number.")
        return None
        
    item_number = int(selection)
    if item_number < 1 or item_number > len(inventory):
        print(f"Item number must be between 1 and {len(inventory)}.")
        return None
    return item_number

def main():
    """Run the InverntoryManager menu until the user chooses to exit."""

    inventory = load_inventory(INVENTORY_FILE)

    while True:
        display_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            view_inventory(inventory)
        elif choice == "2":
            add_item(inventory)
            save_inventory(inventory, INVENTORY_FILE)
        elif choice == "3":
            update_quantity(inventory)
            save_inventory(inventory, INVENTORY_FILE)
        elif choice == "4":
            remove_item(inventory)
            save_inventory(inventory, INVENTORY_FILE)
        elif choice == "5":
            search_inventory(inventory)
        elif choice == "6":
            display_summary(inventory)
        elif choice == "7":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()