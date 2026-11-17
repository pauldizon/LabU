
def linear_search(records, keyword):
    """
    LINEAR SEARCH

    Checks each component individually until matching
    records are found.

    Time Complexity: O(n)
    Space Complexity: O(k), where k is the number of matches.
    """

    results = []
    keyword = keyword.lower()

    # Examine every component in the inventory.
    for component in records:
        component_id = component["component_id"].lower()
        name = component["name"].lower()

        # Check whether the keyword appears in the ID or name.
        if keyword in component_id or keyword in name:
            results.append(component)

    return results


def bubble_sort(records, key="name", reverse=False):
    """
    BUBBLE SORT

    Repeatedly compares adjacent elements and swaps
    them when they are in the wrong order.

    Time Complexity: O(n^2) average and worst case.
    Space Complexity: O(n) for the copied list.
    """

    # Copy the records so the original inventory is unchanged.
    sorted_records = records.copy()

    n = len(sorted_records)

    # Compare adjacent records over multiple passes.
    for i in range(n):
        swapped = False

        for j in range(0, n - i - 1):

            # Get the values used for comparison.
            first = sorted_records[j][key]
            second = sorted_records[j + 1][key]

            # Swap when the records are in the wrong order.
            if reverse:
                should_swap = first < second
            else:
                should_swap = first > second

            if should_swap:
                sorted_records[j], sorted_records[j + 1] = (
                    sorted_records[j + 1],
                    sorted_records[j]
                )
                swapped = True

        # Stop early if no swaps occurred during a pass.
        if not swapped:
            break

    return sorted_records


def binary_search(records, target_id):
    """
    BINARY SEARCH

    Locates a component using its Component ID.

    IMPORTANT:
    Binary Search requires the records to be sorted
    by Component ID before searching.

    Time Complexity: O(log n) after sorting.
    Space Complexity: O(1) for the search itself.
    """

    # Sort by Component ID to satisfy the binary search requirement.
    sorted_records = bubble_sort(records, key="component_id")

    target_id = target_id.strip().lower()

    # Set the initial search boundaries.
    left = 0
    right = len(sorted_records) - 1

    # Continue while the search interval is valid.
    while left <= right:

        # Find the middle position.
        middle = (left + right) // 2

        current_id = sorted_records[middle]["component_id"].lower()

        if current_id == target_id:
            return sorted_records[middle]

        elif current_id < target_id:
            # Target must be in the right half.
            left = middle + 1

        else:
            # Target must be in the left half.
            right = middle - 1

    # Return None if the component does not exist.
    return None

