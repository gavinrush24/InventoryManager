# Inventory Manager Testing

| # | Feature | Input or Action | Expected Result | Actual Result | Pass/Fail |

|---|---|---|---|---|---|

| 1 | Load inventory | start the program with no inventory.txt file | return an empty list | returns an empty list '[]' with no error | Pass |

| 2 | View inventory | start the program with an empty inventory (inventory = []) | return a message saying 'no inventory items found' | message returned with no errors | Pass |

| 3 | Adding a valid item | select option 2 and enter name, category and quantity | item gets added to inventory and saved to inventory.txt | Item added to inventory annd saved to inventory.txt | Pass |

| 4 | Rejecting empty item name | select option 2 to add an item and enter a blank line | return a message saying 'name cannot be empty' | message is returned | Pass |

| 5 | Rejecting duplicate item name | select option 2 to add an item and enter a name of an item that already exists in the inventory | return a message saying 'duplicate items are not allowed' | message is returned | Pass |

| 6 | Rejecting nonnumeric quantity | select option 2 to add an item and enter a letter for the quantity | return a message saying 'Quantity must be a nonnegative whole number' | message is returned | Pass |

| 7 | Rejecting a negative quantity | select option 2 to add an item and enter a negative number for the quantity | return a message saying 'Quantity must be a nonnegative whole number' | message is returned | Pass |

| 8 | Updating a valid item | Select option 3, pick an item to update, and update its quantity | update inventory with new quantity and return a confirmation message | inventory was file was updated and confirmation message was returned | Pass |

| 9 | Rejecting an invalid item number | when updating or adding an item choose a number out of the range | exit the function and return a message displaying the valid choices | Returns to main menu and gives error message | Pass |

| 10 | Removing an item | Select option 4, choose an item number from the list | Item is removed from the inventory, a confirmation message with the item's name is displayed, and the change is saved to inventory.txt | Pass |

| 11 | Case-insensitive partial search | Select option 5 and enter part of an item name in different capitalization | Every item whose name contains the search text is displayed, regardless of capitalization | Pass |

| 12 | Searching when no matches exist | Select option 5 and enter text that matches no item name | Message displayed is 'No inventory items matched your search.' | Pass |

| 13 | Verifying the inventory summary | Add a few items with different categories and quantities (include one with quantity 5 or less), then select option 6 | Unique items, total quantity, and low-stock count match the inventory, and each category is listed with the correct number of items | | Pass |

| 14 | Restarting the program and confirming persistence | Add, update, or remove an item, exit with option 7, restart the program, and select option 1 | The inventory shown after restarting matches the inventory before exiting, with all changes still present | Pass |