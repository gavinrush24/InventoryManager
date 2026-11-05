# AI Usage Report

## Tools Used

Claude and ChatGPT

## How AI Was Used

### Homwork 1
- Most functions have some sort of AI use when writing them and a few were mostly written by AI. 
- Used for suggestions in function testing
- helped make sure that each function met its requirments for the homework assignment

### Homework 2
- AI was used to refactor code to make it easily testable
- Also used to create units tests

## Example Prompts

### Homwork 1
```text
can you take this function and help with the few requirements that i havent met

Validation requirements:

The item name cannot be empty.
The category cannot be empty.
The quantity must be a whole number.
The quantity cannot be negative.
The item name may not contain |.
The category may not contain |.
The program must reject a duplicate item name, even if capitalization differs.
```
```text
can you help me make this helper function (select item number) work

def select_item_number(inventory):
    selection = input("Enter the item number to update: ").strip()
    if not selection.isdigit():
        print("Please enter a valid item number.")
        return False
        
    item_number = int(selection)
    if item_number < 1 or item_number > len(inventory):
        print(f"Item number must be between 1 and {len(inventory)}.")
        return False
    return item_number
```

### Homwork 2
```text
take these instructions and refactor the file I give you to make sure the code is easily testable. Then give me a summary of what functions you changed so i can manually look over them
```
```text
can you explain line 69 and how that logic works
```

## Suggestions Accepted

### Homwork 1
I was trying to make a helper function that was used to select an item number and I kept running into issues. Claude suggested that I replace the 'return False' with 'return None' and then set use an if statement to check if item_number is None and then return false and it fixed my issue. 

### Homwork 2
I was trying to figure out where to implement my fixtures and it suggested that I put one to test the different cases for the `test_nonnumeric_quantity_is_rejected` function and i used that suggestion

## Suggestions Rejected or Modified

### Homwork 1
There was one line of code that was suggested by claude but i didnt know how the flow worked and so i changed it into a few lines that I know I would be able to explain. 

Suggestion: 
```text
matches = [item for item in inventory if search_term in item["name"].lower()]
```
Changed to 
```text
matches = []
for item in inventory:
    if search_term in item["name"].lower():
        matches.append(item)
```

### Homwork 2
There were two test functions that AI suggested I use parameterization but It seemed unnecesary so i deleted them

## Verification

### Homwork 1 and 2
- I read through each line of code that Cluade or ChatGPT gave me and Made sure that I knew what each line of code was doing. 
- I also made sure that the recommendations it gave me would work with previous code that I had written already
- tested all possiblities in my testing and everything that AI had suggestion works with no flaws 

## Code Understanding

### Homwork 1
1. Loading the inventory.txt file

```text
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
```

- The function starts by defining a list called 'inventory'
- It then tries to open the file and if no file is found it raises a FileNotFoundError excpetion and returns an empty list
- It then uses a for loop to iterate between all of the line in the file and if the line is empty it skips it using 'continue'
- Each section is seperated by a '|' using .split("|")
- A disctionary is then made to store the items and their name, category, and quantity
- Finally, at the end of the loop, the item (disctionary) is appened to the inventory (list) and stored in the inventory.txt file
- The inventory is returned at ther end of the function 

2. Updating the quantity of an item

```text
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
```

- The function starts by checking whether the inventory is empty or not and returns a message if it is
- Then runs the view_inventory() function
- The function then calls my helper function to chose an item to update and returns false if that number is not an option 
- The user types in the new quantity of the item they want to update
- checks if the item is a whole number or negative and returns false if either of those are true
- It then sets the item to its corresponding item number so the program knows which value to update
- Takes the value of the item quantity from the dictionary and updates it with the new item quantity
- displays a confirmation message with the item that was updated and the new quantity the user entered
- returns true to exit function

### Homwork 2

```text
@pytest.mark.parametrize(
    "item_number",
    [0, -1, 5],
    ids=["zero_rejected", "negative_rejected", "too_large_rejected"],
)
def test_update_quantity_rejects_invalid_item_number(sample_inventory, item_number):
    # Arrange
    original_inventory = [dict(item) for item in sample_inventory]

    # Act
    result = update_item_quantity(sample_inventory, item_number, 7)

    # Assert
    assert result is None
    assert sample_inventory == original_inventory
    ```

    - parameterization is used to test multiple different int cases without having to make multiple different test cases
    - the fixture sample_inventory is used to reduce repeatbility 
    - the original inventory is set so the each dictionary item is put into the original inventory for comparison later
    - the result uses the item numbers from the parameterization to test the invalid cases and make sure they function properly
    - since the item numbers are outside of the permited range the assert is making sure the result to None and setting the sample inventory to the original inventory because it shouldn't change