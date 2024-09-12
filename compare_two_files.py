# Import necessary libraries
import time

# Load data from two files (assuming each file contains one string per line)
def load_data(file_path):
    with open(file_path, 'r') as file:
        return set(line.strip() for line in file)

# Compare two sets of strings
def compare_sets(set1, set2):
    common_elements = set1.intersection(set2)  # Strings present in both sets
    only_in_set1 = set1.difference(set2)       # Strings only in set1
    only_in_set2 = set2.difference(set1)       # Strings only in set2

    return common_elements, only_in_set1, only_in_set2

# Main function
def main(file1, file2):
    start_time = time.time()

    # Load both datasets
    set1 = load_data(file1)
    set2 = load_data(file2)

    # Compare the two sets
    common, only_in_set1, only_in_set2 = compare_sets(set1, set2)

    # Output the results
    print(f"Common elements (in both sets): {len(common)}")
    print(f"Elements only in set 1: {len(only_in_set1)}")
    print(f"Elements only in set 2: {len(only_in_set2)}")

    # Optionally, save the results to a file
    with open('common_elements.txt', 'w') as f:
        f.write("\n".join(common))

    with open('only_in_set1.txt', 'w') as f:
        f.write("\n".join(only_in_set1))

    with open('only_in_set2.txt', 'w') as f:
        f.write("\n".join(only_in_set2))

    print(f"Comparison completed in {time.time() - start_time} seconds")

if __name__ == "__main__":
    # Provide the paths to the two files containing the string sets
    file1 = 'set1.txt'
    file2 = 'set2.txt'
    main(file1, file2)
