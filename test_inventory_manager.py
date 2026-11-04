"""Tests for the CPS 310 Inventory Manager project."""
import pytest
from inventory_manager import(
    load_inventory,
    save_inventory, 
    update_item_quantity, 
    find_matching_items, 
    remove_item_by_number, 
    parse_nonnegative_int, 
    add_item_to_inventory,
    validate_category,
    validate_item_name, 
    calculate_summary
)


@pytest.fixture
def sample_inventory():
    return [
        {"name": "Phone", "category": "Electronics", "quantity": 10},
        {"name": "Laptop", "category": "Electronics", "quantity": 5},
        {"name": "Notebook", "category": "Office", "quantity": 25},
        {"name": "Stapler", "category": "Office", "quantity": 2},
    ]


# Load Inventory Tests
"""Tests for loading inventory data from a file."""

def test_missing_file(tmp_path):
    # Arrange
    test_file = tmp_path / "not_inventory.txt"

    # Act
    result = load_inventory(test_file)

    # Assert
    assert result == []


def test_loading_empty_file(tmp_path):
    # Arrange
    test_file = tmp_path / "inventory.txt"
    test_file.write_text("")

    # Act
    result = load_inventory(test_file)

    # Assert
    assert result == []


def test_blank_lines_ignored(tmp_path):
    # Arrange
    test_file = tmp_path / "inventory.txt"
    test_file.write_text(
        "\n"
        "Phone|Electronics|10\n"
        "\n"
        "Notebook|Office|25\n"
    )
 
    # Act
    result = load_inventory(test_file)
 
    # Assert
    assert result == [
        {"name": "Phone", "category": "Electronics", "quantity": 10},
        {"name": "Notebook", "category": "Office", "quantity": 25},
    ]


def test_quantities_converted_to_integer(tmp_path):
    # Arrange
    test_file = tmp_path / "inventory.txt"
    test_file.write_text(
        "Phone|Electronics|10\n"
        "Stapler|Office|0\n"
    )
 
    # Act
    result = load_inventory(test_file)
 
    # Assert
    assert len(result) == 2
    assert isinstance(result[0]["quantity"], int)
    assert isinstance(result[1]["quantity"], int)
    assert result[0]["quantity"] == 10
    assert result[1]["quantity"] == 0


def test_valid_inventory_loaded_correctly(tmp_path):
    # Arrange
    test_file = tmp_path / "inventory.txt"
    test_file.write_text(
        "Phone|Electronics|10\n"
        "Laptop|Electronics|5\n"
        "Notebook|Office|25\n"
    )
 
    # Act
    result = load_inventory(test_file)
 
    # Assert
    assert result == [
        {"name": "Phone", "category": "Electronics", "quantity": 10},
        {"name": "Laptop", "category": "Electronics", "quantity": 5},
        {"name": "Notebook", "category": "Office", "quantity": 25},
    ]


# Save Inventory Tests
"""Tests for saving inventory data to a file."""

def test_items_written_in_correct_format(tmp_path, sample_inventory):
    # Arrange
    test_file = tmp_path / "inventory.txt"
 
    # Act
    save_inventory(sample_inventory, test_file)
 
    # Assert
    assert test_file.read_text(encoding="utf-8") == (
        "Phone|Electronics|10\n"
        "Laptop|Electronics|5\n"
        "Notebook|Office|25\n"
        "Stapler|Office|2\n"
    )


def test_saving_empty_inventory(tmp_path):
    # Arrange
    test_file = tmp_path / "inventory.txt"
 
    # Act
    save_inventory([], test_file)
 
    # Assert
    assert test_file.exists()
    assert test_file.read_text(encoding="utf-8") == ""


def test_data_saved_and_loaded_again(tmp_path, sample_inventory):
    # Arrange
    test_file = tmp_path / "inventory.txt"
 
    # Act
    save_inventory(sample_inventory, test_file)
    loaded_inventory = load_inventory(test_file)
 
    # Assert
    assert loaded_inventory == sample_inventory

# Search tests
"""Tests for searching the inventory"""

def test_exact_name_search_finds_correct_item(sample_inventory):
    # Arrange
    search_term = "Phone"
 
    # Act
    result = find_matching_items(sample_inventory, search_term)
 
    # Assert
    assert result == [
        {"name": "Phone", "category": "Electronics", "quantity": 10}
    ]
 
 
def test_partial_search_finds_matching_item(sample_inventory):
    # Arrange
    search_term = "book"
 
    # Act
    result = find_matching_items(sample_inventory, search_term)
 
    # Assert
    assert result == [
        {"name": "Notebook", "category": "Office", "quantity": 25}
    ]
 
 
def test_search_ignores_capitalization(sample_inventory):
    # Arrange
    search_term = "PHONE"
    expected = [{"name": "Phone", "category": "Electronics", "quantity": 10}]
 
    # Act
    result = find_matching_items(sample_inventory, search_term)
 
    # Assert
    assert result == expected
 
 
def test_search_returns_multiple_matching_items(sample_inventory):
    # Arrange
    search_term = "o"  # Phone, Laptop, Notebook
 
    # Act
    result = find_matching_items(sample_inventory, search_term)
 
    # Assert
    assert result == [
        {"name": "Phone", "category": "Electronics", "quantity": 10},
        {"name": "Laptop", "category": "Electronics", "quantity": 5},
        {"name": "Notebook", "category": "Office", "quantity": 25},
    ]
 
 
def test_search_with_no_matches_returns_empty_list(sample_inventory):
    # Arrange
    search_term = "hammer"
 
    # Act
    result = find_matching_items(sample_inventory, search_term)
 
    # Assert
    assert result == []
 
 
def test_empty_or_whitespace_search_returns_empty_list(sample_inventory):
    # Arrange
    search_term = ""
 
    # Act
    result = find_matching_items(sample_inventory, search_term)
 
    # Assert
    assert result == []

# Remove item tests
"""Tests for removing items from the inventory."""

def test_remove_first_item(sample_inventory):
    # Arrange
    item_number = 1
 
    # Act
    removed_item = remove_item_by_number(sample_inventory, item_number)
 
    # Assert
    assert removed_item == {
        "name": "Phone", "category": "Electronics", "quantity": 10
    }
    assert sample_inventory == [
        {"name": "Laptop", "category": "Electronics", "quantity": 5},
        {"name": "Notebook", "category": "Office", "quantity": 25},
        {"name": "Stapler", "category": "Office", "quantity": 2},
    ]
 
 
def test_remove_middle_item(sample_inventory):
    # Arrange
    item_number = 2
 
    # Act
    removed_item = remove_item_by_number(sample_inventory, item_number)
 
    # Assert
    assert removed_item == {
        "name": "Laptop", "category": "Electronics", "quantity": 5
    }
    assert sample_inventory == [
        {"name": "Phone", "category": "Electronics", "quantity": 10},
        {"name": "Notebook", "category": "Office", "quantity": 25},
        {"name": "Stapler", "category": "Office", "quantity": 2},
    ]
 
 
def test_remove_last_item(sample_inventory):
    # Arrange
    item_number = 4
 
    # Act
    removed_item = remove_item_by_number(sample_inventory, item_number)
 
    # Assert
    assert removed_item == {
        "name": "Stapler", "category": "Office", "quantity": 2
    }
    assert sample_inventory == [
        {"name": "Phone", "category": "Electronics", "quantity": 10},
        {"name": "Laptop", "category": "Electronics", "quantity": 5},
        {"name": "Notebook", "category": "Office", "quantity": 25},
    ]
 
 
@pytest.mark.parametrize(
    "item_number",
    [0, -1, 5],
    ids=["zero_rejected", "negative_rejected", "too_large_rejected"],
)
def test_remove_item_rejects_invalid_number(sample_inventory, item_number):
    # Arrange
    original_inventory = [dict(item) for item in sample_inventory]
 
    # Act
    result = remove_item_by_number(sample_inventory, item_number)
 
    # Assert
    assert result is None
    assert sample_inventory == original_inventory


# Update Quantity Tests
"""Tests for updating item quantities in the inventory."""

def test_update_quantity_of_valid_item(sample_inventory):
    # Arrange
    item_number = 2
    new_quantity = 8

    # Act
    updated_item = update_item_quantity(
        sample_inventory, item_number, new_quantity
    )

    # Assert
    assert updated_item == {
        "name": "Laptop", "category": "Electronics", "quantity": 8
    }
    assert sample_inventory[1]["quantity"] == 8


def test_update_quantity_accepts_zero(sample_inventory):
    # Arrange
    item_number = 4
    new_quantity = 0

    # Act
    updated_item = update_item_quantity(
        sample_inventory, item_number, new_quantity
    )

    # Assert
    assert updated_item is not None
    assert sample_inventory[3]["quantity"] == 0


def test_update_quantity_changes_only_the_selected_item(sample_inventory):
    # Arrange
    item_number = 3
    new_quantity = 40

    # Act
    update_item_quantity(sample_inventory, item_number, new_quantity)

    # Assert
    assert sample_inventory == [
        {"name": "Phone", "category": "Electronics", "quantity": 10},
        {"name": "Laptop", "category": "Electronics", "quantity": 5},
        {"name": "Notebook", "category": "Office", "quantity": 40},
        {"name": "Stapler", "category": "Office", "quantity": 2},
    ]


@pytest.mark.parametrize(
    "item_number",
    [0, -1, 5],
    ids=["zero_rejected", "negative_rejected", "too_large_rejected"],
)
def test_update_quantity_rejects_invalid_item_number(
    sample_inventory, item_number
):
    # Arrange
    original_inventory = [dict(item) for item in sample_inventory]

    # Act
    result = update_item_quantity(sample_inventory, item_number, 7)

    # Assert
    assert result is None
    assert sample_inventory == original_inventory


def test_update_quantity_rejects_negative_quantity(sample_inventory):
    # Arrange
    original_inventory = [dict(item) for item in sample_inventory]

    # Act
    result = update_item_quantity(sample_inventory, 1, -5)

    # Assert
    assert result is None
    assert sample_inventory == original_inventory


def test_parse_nonnegative_int_rejects_negative_quantity_text():
    # Arrange
    quantity_text = "-5"

    # Act
    result = parse_nonnegative_int(quantity_text)

    # Assert
    assert result is None


# Add-Item validation tests
"""Tests for validating new inventory items."""

def test_valid_item_passes_all_validation(sample_inventory):
    # Arrange
    name = "Tablet"
    category = "Electronics"
    quantity_text = "12"

    # Act
    name_error = validate_item_name(sample_inventory, name)
    category_error = validate_category(category)
    quantity = parse_nonnegative_int(quantity_text)

    # Assert
    assert name_error is None
    assert category_error is None
    assert quantity == 12


def test_add_item_to_inventory_appends_new_item(sample_inventory):
    # Arrange
    name = "  Tablet "
    category = " Electronics  "
    quantity = 12

    # Act
    added_item = add_item_to_inventory(sample_inventory, name, category, quantity)

    # Assert
    expected_item = {"name": "Tablet", "category": "Electronics", "quantity": 12}
    assert added_item == expected_item
    assert len(sample_inventory) == 5
    assert sample_inventory[-1] == expected_item


def test_empty_item_name_is_rejected(sample_inventory):
    # Arrange
    name = ""

    # Act
    error = validate_item_name(sample_inventory, name)

    # Assert
    assert error == "Item name cannot be empty."


def test_empty_category_is_rejected(sample_inventory):
    # Arrange
    category = ""

    # Act
    error = validate_category(category)

    # Assert
    assert error == "Category cannot be empty."


def test_pipe_in_item_name_is_rejected(sample_inventory):
    # Arrange
    name = "Smart|Watch"

    # Act
    error = validate_item_name(sample_inventory, name)

    # Assert
    assert error == "Item name may not contain the | character."


def test_pipe_in_category_is_rejected():
    # Arrange
    category = "Home|Office"

    # Act
    error = validate_category(category)

    # Assert
    assert error == "Category may not contain the | character."


def test_negative_quantity_is_rejected():
    # Arrange
    quantity_text = "-5"

    # Act
    quantity = parse_nonnegative_int(quantity_text)

    # Assert
    assert quantity is None


@pytest.mark.parametrize(
    "quantity_text",
    ["abc", "12abc", "3.5", ""],
    ids=["letters", "digits_then_letters", "decimal", "empty"],
)
def test_nonnumeric_quantity_is_rejected(quantity_text):
    # Arrange
    # (quantity_text is provided by pytest)

    # Act
    quantity = parse_nonnegative_int(quantity_text)

    # Assert
    assert quantity is None


def test_duplicate_item_name_is_rejected(sample_inventory):
    # Arrange
    name = "Phone"

    # Act
    error = validate_item_name(sample_inventory, name)

    # Assert
    assert error == "An item with that name already exists."


def test_duplicate_item_name_with_different_capitalization_is_rejected(sample_inventory):
    # Arrange
    name = "PHONE"

    # Act
    error = validate_item_name(sample_inventory, name)

    # Assert
    assert error == "An item with that name already exists."


# Inventory Summary Tests
"""Tests for inventory summary calculations."""

def test_summary_counts_unique_items(sample_inventory):
    # Arrange
    # (sample_inventory is provided by the fixture)

    # Act
    summary = calculate_summary(sample_inventory)

    # Assert
    assert summary["unique_items"] == 4


def test_summary_calculates_total_quantity(sample_inventory):
    # Arrange
    # (10 + 5 + 25 + 2 = 42)

    # Act
    summary = calculate_summary(sample_inventory)

    # Assert
    assert summary["total_quantity"] == 42


def test_summary_counts_low_stock_items(sample_inventory):
    # Arrange
    # (only Stapler, quantity 2, is below 5)

    # Act
    summary = calculate_summary(sample_inventory)

    # Assert
    assert summary["low_stock_items"] == 1


@pytest.mark.parametrize(
    "quantity, expected_low_stock_count",
    [
        (4, 1),
        (5, 0),
    ],
    ids=["quantity_4_is_low_stock", "quantity_5_is_not_low_stock"],
)
def test_low_stock_boundary(quantity, expected_low_stock_count):
    # Arrange
    inventory = [{"name": "Widget", "category": "Parts", "quantity": quantity}]

    # Act
    summary = calculate_summary(inventory)

    # Assert
    assert summary["low_stock_items"] == expected_low_stock_count


def test_summary_counts_items_by_category(sample_inventory):
    # Arrange
    # (2 Electronics items and 2 Office items)

    # Act
    summary = calculate_summary(sample_inventory)

    # Assert
    assert summary["category_counts"] == {"Electronics": 2, "Office": 2}


def test_category_counts_ignore_capitalization():
    # Arrange
    inventory = [
        {"name": "Phone", "category": "Electronics", "quantity": 10},
        {"name": "Laptop", "category": "electronics", "quantity": 5},
        {"name": "Tablet", "category": "ELECTRONICS", "quantity": 7},
        {"name": "Stapler", "category": "Office", "quantity": 2},
    ]

    # Act
    summary = calculate_summary(inventory)

    # Assert
    assert summary["category_counts"] == {"Electronics": 3, "Office": 1}


def test_empty_inventory_summary():
    # Arrange
    inventory = []

    # Act
    summary = calculate_summary(inventory)

    # Assert
    assert summary == {
        "unique_items": 0,
        "total_quantity": 0,
        "low_stock_items": 0,
        "category_counts": {},
    }
