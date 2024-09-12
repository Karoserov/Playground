import pandas as pd

# File paths
file1_path = 'D:\\SOS-93\\persons_non_applicable_disability_types_with_refs.csv'
# The file with 'id' and 'ref' columns
file2_path = 'D:\\SOS-93\\persons_non_applicable_disability_types.csv'
# The file with 'id', 'chrn', 'person_group', 'disability_type' columns
report_path = 'D:\\SOS-93\\non_configured_disability_types.csv'  # The path to save the report

# Load CSV files into DataFrames
df1 = pd.read_csv(file1_path, delimiter=';')
df2 = pd.read_csv(file2_path, delimiter=';')

# Print column names for debugging
print("File 1 columns:", df1.columns)
print("File 2 columns:", df2.columns)

# Remove leading/trailing spaces from column names
df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()

# Print column names again after stripping spaces
print("File 1 columns after stripping spaces:", df1.columns)
print("File 2 columns after stripping spaces:", df2.columns)

# Merge the DataFrames on the 'id' column
merged_df = pd.merge(df2, df1, on='id', how='left')

# Create the report DataFrame with the desired columns
report_df = merged_df[['id', 'chrn', 'person_group', 'disability_type', 'ref']]

# Save the report to a CSV file
report_df.to_csv(report_path, index=False)

print(f'Report generated and saved to {report_path}')