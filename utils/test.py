# write a code to sot a list
def sort_list(input_list):
    """
    Sorts a list in ascending order.
    
    Args:
        input_list (list): The list to be sorted.
        
    Returns:
        list: A new list containing the sorted elements.
    """
    if not isinstance(input_list, list):
        raise TypeError("Input must be a list")
    
    return sorted(input_list)

# Example usage 
if __name__ == "__main__":
    sample_list = [5, 2, 9, 1, 5, 6]
    sorted_list = sort_list(sample_list)
    print("Original list:", sample_list)
    print("Sorted list:", sorted_list)
    
    # Testing with an invalid input
    try:
        sort_list("not a list")
    except TypeError as e:
        print("Error:", e)