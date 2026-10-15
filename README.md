# Inventory Manager

## Project Description

Inventory Manager is a command-line Python application that stores, searches, updates, and summarizes inventory data.

## Current Features 

- Display main menu
- Add item to inventory (name, category, and quantity)
- Display items you have added to inventory
- Update the quantity of an existing item
- Remove an item from the inventory
- Search for an item in the inventory
- Display a short summary of the inventory including unique items, total quantity, low stock items, etc.

## Requirements

- Python 3

## Project Files

- `inventory_manager.py` — Main python code that handles menu options, adding, removing, and updating items as well as file I/O

- `inventory.txt` — File storing the item information once added to the inventory

- `.gitignore` — Any type of file that you want Git to ignore when committing and pushing 

- `TESTING.md` — Documentation on tests performed to ensure the program runs smoothly with no bugs or errors

- `AI_USAGE.md` — Documentation on what sort of AI tools were used and how they assisted in making this program

## Inventory Data Format
```text
Item|Category|Quantity(int)
```
inventory.txt stores one item per line 

## Instructions for running the program

Run ` python inventory_manager.py` in the terminal 

## Menu options
 ```text 
 InventoryManager Menu
1. View Inventory
2. Add an item
3. Update an item quantity
4. Remove an item
5. Search inventory
6. View inventory summary
7. Exit
```

## Sample interaction
```text
InventoryManager Menu
1. View Inventory
2. Add an item
3. Update an item quantity
4. Remove an item
5. Search inventory
6. View inventory summary
7. Exit
Choose an option: 1
Inventory:
1. Phone | Electronics | Quantity: 3
2. Apple Watch | Electronics | Quantity: 6
3. Paper Clips | Office Supplies | Quantity: 13
4. Watermelon | Groceries | Quantity: 4

InventoryManager Menu
1. View Inventory
2. Add an item
3. Update an item quantity
4. Remove an item
5. Search inventory
6. View inventory summary
7. Exit
Choose an option: 2
Enter item name: Laptop
Enter the category: Electronics
Enter the quantity: 2
Item added successfully.

InventoryManager Menu
1. View Inventory
2. Add an item
3. Update an item quantity
4. Remove an item
5. Search inventory
6. View inventory summary
7. Exit
Choose an option: 6
Inventory Summary
Unique items: 5
Total quantity: 28
Low-stock items: 3

Items by category: 
Electronics: 3
Office Supplies: 1
Groceries: 1

InventoryManager Menu
1. View Inventory
2. Add an item
3. Update an item quantity
4. Remove an item
5. Search inventory
6. View inventory summary
7. Exit
Choose an option: 7
Goodbye!
```

## Testing Summary

TESTING.md lists 14 manual test cases, each with the action taken, the expected result, the actual result, and Pass/Fail.

No automated tests were done

## Git/GitHub Development Summary

 - Repository: https://github.com/gavinrush24/InventoryManager

 - The project was built in stages with a commit after each completed feature

 - An issue was created to implement a search inventory feature
 - A branch was used when developing the 'search inventory' function

## Known Limitations

- Only the quantity of an existing item can be changed
- search only checks for names and not categories
- if the inventory file is edited by hand and is not in the proper format, loading the file will fail
- names and categories cannot contain '|' because it is used in formatting in the inventory file

## Possible Future Improvements 

- be able to edit an item's name and category
- search by category as well as name
- skip lines that are not formatted in the correct way when loading the file
- be able to sort the inventory by either category or quantity