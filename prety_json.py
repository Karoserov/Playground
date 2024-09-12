import json

# Read the JSON file
with open('data.csv', 'r') as file:
    data = json.load(file)

# Write the expanded JSON to a new file
with open('pretty_data.csv', 'w') as file:
    json.dump(data, file, indent=4)
