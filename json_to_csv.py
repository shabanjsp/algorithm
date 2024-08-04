import json
import csv
import os

# Specify the input and output directories
input_folder = 'filtered_results3'
output_folder = 'csv3'
output_csv = 'combined_listings.csv'

# Create the output directory if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Initialize a list to hold all listings and a set to hold all fieldnames
all_listings = []
all_fieldnames = set()

# Iterate over all files in the input directory
for json_file in os.listdir(input_folder):
    if json_file.endswith('.json'):
        # Extract the numeric part of the filename
        base_filename = os.path.splitext(json_file)[0]
        try:
            fortyeight = (int(base_filename) - 1) * 48
            # multiplier = (int(base_filename) - 1) * 48
            if int(base_filename) == 1:
                multiplier = 1
        except ValueError:
            print(f"Skipping file {json_file} as the filename is not a numeric value")
            continue

        # Construct the full path to the JSON file
        json_path = os.path.join(input_folder, json_file)
        
        # Read JSON data from file
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        # Check the structure of the JSON data
        if 'listings' not in data:
            raise ValueError(f"Invalid JSON format in file {json_file}: 'listings' key not found")
        
        # Extract listings
        listings = data['listings']
        
        # Check if listings is a list
        if not isinstance(listings, list):
            raise ValueError(f"Invalid JSON format in file {json_file}: 'listings' should be a list")
        
        # Modify the 'pos' field and collect fieldnames
        for listing in listings:

            


            if int(base_filename) == 1:
                fortyeight = 0





            listing['pos'] = listing['pos'] + fortyeight
            all_fieldnames.update(listing.keys())
        
        # Add the modified listings to the all_listings list
        all_listings.extend(listings)

# Get the headers from the collected fieldnames
headers = list(all_fieldnames)

# Write all listings to a single CSV file
with open(os.path.join(output_folder, output_csv), 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    for listing in all_listings:
        writer.writerow(listing)

print(f"All data has been written to the single CSV file: '{output_csv}' in the '{output_folder}' folder")
