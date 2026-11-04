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