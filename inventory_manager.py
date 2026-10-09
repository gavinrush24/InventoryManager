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
    ...

def update_quantity(inventory):
    ...

def remove_item(inventory):
    ...

def search_inventory(inventory):
    ...

def display_summary(inventory):
    ...

def main():
    """Run the InverntoryManager menu until the user chooses to exit."""
    inventory = load_inventory(INVENTORY_FILE)
    while True:
        display_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            view_inventory(inventory)

        elif choice == "2":
            ...
        elif choice == "3":
            ...
        elif choice == "4":
            ...
        elif choice == "5":
            ...
        elif choice == "6":
            ...
        elif choice == "7":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()