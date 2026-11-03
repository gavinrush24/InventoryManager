"""CPS 310 - Homework 2: Inventory Manager
Refactored so important logic lives in small, directly testable helpers.
"""

INVENTORY_FILE = "inventory.txt"
LOW_STOCK_THRESHOLD = 5


# ---------------------------------------------------------------------------
# Menu display
# ---------------------------------------------------------------------------

def display_menu():
    """Display the main Inventory Manager menu."""
    print("\nInventory Manager")
    print("1. View inventory")
    print("2. Add an item")
    print("3. Update an item quantity")
    print("4. Remove an item")
    print("5. Search inventory")
    print("6. View inventory summary")
    print("7. Exit")


# ---------------------------------------------------------------------------
# File handling
# ---------------------------------------------------------------------------

def load_inventory(filename):
    """Load inventory records from a pipe-delimited text file."""
    inventory = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                name, category, quantity = line.split("|")
                inventory.append(
                    {
                        "name": name,
                        "category": category,
                        "quantity": int(quantity),
                    }
                )
    except FileNotFoundError:
        return []

    return inventory


def save_inventory(inventory, filename):
    """Save the complete inventory to a pipe-delimited text file."""
    with open(filename, "w", encoding="utf-8") as file:
        for item in inventory:
            file.write(
                f'{item["name"]}|{item["category"]}|{item["quantity"]}\n'
            )


# ---------------------------------------------------------------------------
# Testable helpers (no input(), no print(), no file access)
# ---------------------------------------------------------------------------

def parse_nonnegative_int(text):
    """Return text as an int if it is a nonnegative whole number, else None."""
    text = text.strip()
    if not (text.isascii() and text.isdigit()):
        return None
    return int(text)


def format_item_line(index, item):
    """Return the display line for one inventory item."""
    return (
        f'{index}. {item["name"]} | {item["category"]} | '
        f'Quantity: {item["quantity"]}'
    )


def validate_item_name(inventory, name):
    """Return an error message if name is not acceptable, else None."""
    name = name.strip()
    if not name:
        return "Item name cannot be empty."
    if "|" in name:
        return "Item name may not contain the | character."
    for item in inventory:
        if item["name"].lower() == name.lower():
            return "An item with that name already exists."
    return None


def validate_category(category):
    """Return an error message if category is not acceptable, else None."""
    category = category.strip()
    if not category:
        return "Category cannot be empty."
    if "|" in category:
        return "Category may not contain the | character."
    return None


def add_item_to_inventory(inventory, name, category, quantity):
    """Append a new item to the inventory and return it.

    Assumes the values were already validated.
    """
    item = {
        "name": name.strip(),
        "category": category.strip(),
        "quantity": quantity,
    }
    inventory.append(item)
    return item


def validate_item_number(inventory, item_number):
    """Return an error message if item_number is not a valid 1-based
    position in the inventory, else None."""
    if (
        not isinstance(item_number, int)
        or item_number < 1
        or item_number > len(inventory)
    ):
        return "Item number is outside the available range."
    return None


def update_item_quantity(inventory, item_number, new_quantity):
    """Set the quantity of the item at the 1-based item_number.

    Returns the updated item, or None if the item number or quantity is
    invalid (in which case the inventory is not changed).
    """
    if validate_item_number(inventory, item_number) is not None:
        return None
    if not isinstance(new_quantity, int) or new_quantity < 0:
        return None

    item = inventory[item_number - 1]
    item["quantity"] = new_quantity
    return item


def remove_item_by_number(inventory, item_number):
    """Remove the item at the 1-based item_number from the inventory.

    Returns the removed item, or None if the item number is invalid (in
    which case the inventory is not changed).
    """
    if validate_item_number(inventory, item_number) is not None:
        return None
    return inventory.pop(item_number - 1)


def find_matching_items(inventory, search_term):
    """Return all items whose name contains search_term (case-insensitive).

    An empty or whitespace-only search term matches nothing.
    """
    search_term = search_term.strip().lower()
    if not search_term:
        return []

    matches = []
    for item in inventory:
        if search_term in item["name"].lower():
            matches.append(item)
    return matches


def calculate_summary(inventory):
    """Return a dictionary of inventory summary information.

    Keys:
        "unique_items"    - number of items
        "total_quantity"  - sum of all quantities
        "low_stock_items" - number of items below LOW_STOCK_THRESHOLD
        "category_counts" - {category label: item count}; categories are
                            grouped case-insensitively and labeled with the
                            first spelling encountered
    """
    total_quantity = 0
    low_stock_items = 0
    category_counts = {}
    category_labels = {}

    for item in inventory:
        total_quantity += item["quantity"]

        if item["quantity"] < LOW_STOCK_THRESHOLD:
            low_stock_items += 1

        category_key = item["category"].lower()
        if category_key not in category_counts:
            category_counts[category_key] = 0
            category_labels[category_key] = item["category"]
        category_counts[category_key] += 1

    labeled_counts = {}
    for category_key, count in category_counts.items():
        labeled_counts[category_labels[category_key]] = count

    return {
        "unique_items": len(inventory),
        "total_quantity": total_quantity,
        "low_stock_items": low_stock_items,
        "category_counts": labeled_counts,
    }


# ---------------------------------------------------------------------------
# Interactive functions (input() / print() / saving live here)
# ---------------------------------------------------------------------------

def view_inventory(inventory):
    """Display all inventory items in a numbered list."""
    if not inventory:
        print("No inventory items found.")
        return

    print("\nInventory:")
    for index, item in enumerate(inventory, start=1):
        print(format_item_line(index, item))


def add_item(inventory):
    """Prompt for and add one validated inventory item, then save it."""
    name = input("Enter the item name: ").strip()
    error = validate_item_name(inventory, name)
    if error:
        print(error)
        return

    category = input("Enter the category: ").strip()
    error = validate_category(category)
    if error:
        print(error)
        return

    quantity = parse_nonnegative_int(input("Enter the quantity: "))
    if quantity is None:
        print("Quantity must be a nonnegative whole number.")
        return

    add_item_to_inventory(inventory, name, category, quantity)
    save_inventory(inventory, INVENTORY_FILE)
    print("Item added successfully.")


def update_quantity(inventory):
    """Prompt for an item number and replace its quantity, then save it."""
    if not inventory:
        print("No inventory items found.")
        return

    view_inventory(inventory)
    item_number = parse_nonnegative_int(
        input("Enter the item number to update: ")
    )
    if item_number is None:
        print("Item number must be a valid whole number.")
        return

    error = validate_item_number(inventory, item_number)
    if error:
        print(error)
        return

    quantity = parse_nonnegative_int(input("Enter the new quantity: "))
    if quantity is None:
        print("Quantity must be a nonnegative whole number.")
        return

    item = update_item_quantity(inventory, item_number, quantity)
    save_inventory(inventory, INVENTORY_FILE)
    print(f'{item["name"]} quantity updated to {quantity}.')


def remove_item(inventory):
    """Prompt for an item number, remove that item, then save the inventory."""
    if not inventory:
        print("No inventory items found.")
        return

    view_inventory(inventory)
    item_number = parse_nonnegative_int(
        input("Enter the item number to remove: ")
    )
    if item_number is None:
        print("Item number must be a valid whole number.")
        return

    error = validate_item_number(inventory, item_number)
    if error:
        print(error)
        return

    removed_item = remove_item_by_number(inventory, item_number)
    save_inventory(inventory, INVENTORY_FILE)
    print(f'Item removed: {removed_item["name"]}')


def search_inventory(inventory):
    """Prompt for an item-name search term and display matching items."""
    search_term = input("Enter part or all of an item name: ").strip()
    if not search_term:
        print("Search term cannot be empty.")
        return

    matches = find_matching_items(inventory, search_term)
    if not matches:
        print("No inventory items matched your search.")
        return

    print("\nSearch Results:")
    for index, item in enumerate(matches, start=1):
        print(format_item_line(index, item))


def display_summary(inventory):
    """Display inventory summary information."""
    summary = calculate_summary(inventory)

    print("\nInventory Summary")
    print(f"Unique items: {summary['unique_items']}")
    print(f"Total quantity: {summary['total_quantity']}")
    print(f"Low-stock items: {summary['low_stock_items']}")
    print("\nItems by category:")

    if not summary["category_counts"]:
        print("No categories found.")
        return

    for category, count in summary["category_counts"].items():
        print(f"{category}: {count}")


def main():
    """Run the Inventory Manager menu loop."""
    inventory = load_inventory(INVENTORY_FILE)

    while True:
        display_menu()
        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            view_inventory(inventory)
        elif choice == "2":
            add_item(inventory)
        elif choice == "3":
            update_quantity(inventory)
        elif choice == "4":
            remove_item(inventory)
        elif choice == "5":
            search_inventory(inventory)
        elif choice == "6":
            display_summary(inventory)
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Please enter a menu option from 1 through 7.")


if __name__ == "__main__":
    main()