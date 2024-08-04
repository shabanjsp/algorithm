import json
import os

# Define the input and output directories
input_directory = 'results3'
output_directory = 'filtered_results3'

# Create the output directory if it does not exist
os.makedirs(output_directory, exist_ok=True)

# Iterate over all JSON files in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.json'):
        input_path = os.path.join(input_directory, filename)
        
        try:
            # Open the file with UTF-8 encoding
            with open(input_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            # Extract the relevant information
            filtered_listings = []
            for listing in data.get('listings', []):
                if listing.get('gigs', []):
                    for gig in listing.get('gigs', []):
                        filtered_gig = {
                            "pos": gig.get("pos"),
                            "is_fiverr_choice": gig.get("is_fiverr_choice"),
                            "seller_name": gig.get("seller_name"),
                            "seller_country": gig.get("seller_country"),
                            "seller_level": gig.get("seller_level"),
                            "is_pro": gig.get("is_pro"),
                            "buying_review_rating_count": gig.get("buying_review_rating_count"),
                            "buying_review_rating": gig.get("buying_review_rating"),
                            "price_i": gig.get("price_i"),
                            "count": gig.get("seller_rating", {}).get("count"),
                            "score": gig.get("seller_rating", {}).get("score")
                        }
                        filtered_listings.append(filtered_gig)
                if listing.get('roles', []):
                    for gig in listing.get('roles', []):
                        filtered_gig = {
                            "pos": gig.get("position"),
                            "is_fiverr_choice": False,

                            "seller_name": gig.get("seller", {}).get("username"),
                            "seller_country": gig.get("seller", {}).get("countryCode"),
                            "seller_level": gig.get("seller", {}).get("level"),

                            "is_pro": gig.get("role", {}).get("isPro"),
                            "buying_review_rating_count": gig.get("role", {}).get("ordersAmount"),
                            "buying_review_rating": gig.get("role", {}).get("review", {}).get("score"),
                            "price_i": gig.get("role", {}).get("minPrice"),                            
                            "count": gig.get("role", {}).get("review", {}).get("count"),
                            "score": gig.get("role", {}).get("review", {}).get("score")
                        }
                        filtered_listings.append(filtered_gig)                    


            
            # Create a new JSON file with the filtered data
            filtered_data = {
                "listings": filtered_listings
            }
            
            output_path = os.path.join(output_directory, filename)
            with open(output_path, 'w', encoding='utf-8') as file:
                json.dump(filtered_data, file, indent=4)
            
            print(f"Filtered JSON file '{filename}' has been created successfully.")
        
        except UnicodeDecodeError as e:
            print(f"Error decoding file '{filename}': {e}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file '{filename}': {e}")
        except Exception as e:
            print(f"An unexpected error occurred with file '{filename}': {e}")

print("All JSON files have been processed.")
