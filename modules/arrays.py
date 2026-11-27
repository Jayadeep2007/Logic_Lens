
# modules/arrays.py

def create_array(values):
    """Create an array from user-provided values."""
    return list(values)


def insert_element(arr, index, value):
    if index < 0 or index > len(arr):
        raise IndexError("Invalid insertion index")

    result = arr.copy()
    result.insert(index, value)
    return result


def delete_element(arr, index):
    if index < 0 or index >= len(arr):
        raise IndexError("Invalid deletion index")

    result = arr.copy()
    result.pop(index)
    return result


def update_element(arr, index, value):
    if index < 0 or index >= len(arr):
        raise IndexError("Invalid update index")

    result = arr.copy()
    result[index] = value
    return result


def search_element(arr, target):
    for index, value in enumerate(arr):
        if value == target:
            return index
    return -1


def sort_array(arr):
    return sorted(arr)


def reverse_array(arr):
    return arr[::-1]


def bubble_sort_steps(arr):
    """Return every intermediate state of bubble sort."""

    result = arr.copy()
    steps = [result.copy()]

    n = len(result)

    for i in range(n):
        swapped = False

        for j in range(0, n - i - 1):

            if result[j] > result[j + 1]:

                result[j], result[j + 1] = (
                    result[j + 1],
                    result[j]
                )

                steps.append(result.copy())
                swapped = True

        if not swapped:
            break

    return steps


def reverse_steps(arr):
    """Return intermediate states while reversing."""

    result = arr.copy()
    steps = [result.copy()]

    left = 0
    right = len(result) - 1

    while left < right:

        result[left], result[right] = (
            result[right],
            result[left]
        )

        steps.append(result.copy())

        left += 1
        right -= 1

    return steps
