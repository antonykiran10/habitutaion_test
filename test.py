import re

# Sample list of filenames
filenames = ["file1.txt", "file10.txt", "file2.txt", "file20.txt"]

# Define a custom sorting function
def sort_by_numbers(filename):
    # Extract numbers from the filename
    numbers = re.findall(r'\d+', filename)
    # Convert the numbers to integers for proper numerical sorting
    return int(numbers[0]) if numbers else float('inf')

# Sort the filenames based on the numbers extracted
sorted_filenames = sorted(filenames, key=sort_by_numbers)

# Print the sorted list
print(sorted_filenames)