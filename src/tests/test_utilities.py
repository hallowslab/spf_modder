from spf_utilities import remove_duplicate_entries  # Import your function from your module

def test_remove_duplicates_empty_dict():
    # Test for an empty dictionary input
    records_dict = {}
    result = remove_duplicate_entries(records_dict)
    assert result == {}  # Expect an empty dictionary as output

def test_remove_duplicates_no_duplicates():
    # Test for a dictionary without any duplicates
    records_dict = {
        'key1': [1, 2, 3],
        'key2': ['a', 'b', 'c']
    }
    result = remove_duplicate_entries(records_dict)
    assert result == records_dict  # Expect the same dictionary as output

def test_remove_duplicates_with_duplicates():
    # Test for a dictionary with duplicate entries
    records_dict = {
        'key1': [1, 2, 2, 3, 3, 4],
        'key2': ['a', 'b', 'b', 'c', 'c', 'd']
    }
    expected_result = {
        'key1': [1, 2, 3, 4],
        'key2': ['a', 'b', 'c', 'd']
    }
    result = remove_duplicate_entries(records_dict)
    assert result == expected_result  # Expect the duplicates to be removed
