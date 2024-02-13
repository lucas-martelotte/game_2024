from typing import Callable


def insertion_sort(arr: list, size: Callable[[object], int]) -> None:
    n = len(arr)  # Get the length of the array

    if n <= 1:
        return  # If the array has 0 or 1 element, it is already sorted, so return

    for i in range(1, n):  # Iterate over the array starting from the second element
        key = arr[
            i
        ]  # Store the current element as the key to be inserted in the right position
        j = i - 1
        while j >= 0 and size(key) < size(arr[j]):
            # Move elements greater than key one position ahead
            arr[j + 1] = arr[j]  # Shift elements to the right
            j -= 1
        arr[j + 1] = key  # Insert the key in the correct position
