import csv
from openpyxl import Workbook


# Function to read CSV and save as Excel with specified delimiter
def csv_to_excel(csv_file, delimiter=',', encoding='utf-8'):
    try:
        # Create a new Excel workbook and sheet
        workbook = Workbook()
        sheet = workbook.active

        # Open the CSV file and read its contents
        with open(csv_file, newline='', encoding=encoding) as csvfile:
            csvreader = csv.reader(csvfile, delimiter=delimiter)

            # Loop through each row in the CSV
            for row in csvreader:
                # Write the row data into the Excel sheet, placing each item in its respective column
                sheet.append(row)  # Appends the row with items split into columns

        # Create the output Excel file name by replacing .csv with .xlsx
        excel_file = csv_file.replace('.csv', '.xlsx')

        # Save the workbook to an Excel file
        workbook.save(excel_file)

        print(f"Successfully converted '{csv_file}' to '{excel_file}' using delimiter '{delimiter}'")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
csv_file = 'data.csv'  # Replace with your CSV file path
delimiter = ','  # Replace with the correct delimiter (',' or ';' or '\t' or '|')
csv_to_excel(csv_file, delimiter)
