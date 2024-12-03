import pandas as pd

# Loading the Excel file
file_path = "Book1.xlsx"
output_file_path = "duplicates_output.xlsx" # if you want to export non-duplicates just put 'non_' in front of the file
df = pd.read_excel(file_path)


# Group by first column and find the unique states from column 3
unique_counts = df.groupby('chrn')['hint'].nunique()

# Filter for entities with more than one unique value
entities_with_duplicates = unique_counts[unique_counts > 1].index # for non-duplicate you just change the state from '>' to '=='

# Filter the original DataFrame for matching entities in Column 1
filtered_df = df[df['chrn'].isin(entities_with_duplicates)]
# Export to a CSV file
filtered_df.to_excel(output_file_path, index=False)

print(f"Results exported to {output_file_path}")

