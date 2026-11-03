"""Tests for the CPS 310 Inventory Manager project."""
import pytest
from inventory_manager import(
    load_inventory,
    save_inventory, 
    search_inventory, 
    remove_item, 
    update_quantity, 
    add_item, 
    display_summary, 
    find_matching_items
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
 
 
@pytest.mark.parametrize("search_term", ["phone", "PHONE", "pHoNe"])
def test_search_ignores_capitalization(sample_inventory, search_term):
    # Arrange
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