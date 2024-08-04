from urllib.parse import urlparse
import requests
import random
import time
import concurrent.futures
import json
import os
import argparse
from colorama import Fore, Style
import functools
import time
import shutil
import tempfile

 
# Read user agents from file
def read_user_agents(file_path='user_agents.txt'):
    try:
        with open(file_path, 'r') as file:
            user_agents = [line.strip() for line in file.readlines()]
        return user_agents
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return []


def generate_random_headers(user_agents):
    try:
        # Randomly choose a user agent
        user_agent = random.choice(user_agents)

        # Create headers with the chosen user agent
        headers = {
            'User-Agent': user_agent,
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/'
        }

      

        return headers

    except IndexError:
        print("Empty list of user agents.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None 


def read_urls_from_file(file_path='urls.txt'):
    try:
        with open(file_path, 'r') as file:
            urls = [line.strip() for line in file.readlines()]
        return urls
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []



def validate_file(file_path):
    if os.path.exists(file_path):
        return True
    else:
        print(f"Error: {file_path} does not exist.")
        return



def process_response(response_text,url=None):
    try:

        # print(response_text)
        # print(response_text)
        
        
        # Find the position where the JSON starts

        start_index = response_text.find('{"isBusiness":')

        # Check if the starting position is found
        if start_index != -1:

            # Extract the substring starting from the found position
            json_data_string = response_text[start_index:]

            # Find the outermost JSON object
            stack = []
            end_index = None

            for i, char in enumerate(json_data_string):
                if char == '{':
                    stack.append(i)
                elif char == '}':
                    stack.pop()
                    if not stack:
                        end_index = i
                        break

            if end_index is not None:
                json_data_string = json_data_string[:end_index + 1]

                # Load the JSON data
                try:
                    json_data = json.loads(json_data_string)
                    
                    return json_data
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
            else:
                print("End of outermost JSON object not found.")
        else:
            print(f"JSON starting point not found for: {url}")
           
    except Exception as ex:
        print(f"An error occurred in response: {ex}")

def make_request(url, headers=None, params=None):
    try:
        proxy_with_auth = {
            'http': 'http://gazfQIdkP5Nj1DNV:KfWUfWjHQ0lzPFrn@geo.iproyal.com:12321',
        }
        response = requests.get(url, headers=headers, params=params, proxies=proxy_with_auth)
        status_code = response.status_code
        response_text = response.text
        
        return status_code, response_text
        
    except requests.RequestException as e:
        # Handle exceptions, you can modify this part based on your needs
        print(f"Request failed with error: {e}")
        return None, None
# temp_dir_path = create_temp_hidden_dir()    






user_agents = read_user_agents()
headers = generate_random_headers(user_agents=user_agents)
urls=read_urls_from_file()
# urls=list(set(urls))
print(f"total urls:{len(urls)}")
for url in urls:



    # print(tmp_urls)
    # process_url_partial = functools.partial(process_url, dir_path=temp_dir_path)

    # with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
    #     executor.map(process_url_partial, tmp_urls)




    
    status_code, response_text = make_request(url, headers=headers)
    json_data = process_response(response_text)
    if json_data:
        # {"isBusiness":false,"isBusinessUser":false,"categoryIds":{"categoryId":"10"
        # {"seller":{"user":{"id":"129632692","name":"victordemaria","
        # file_name=f"{json_data['isBusiness']['categoryId']}.json"
        
        # file_name=f"{i}.json"
        file_name=f"{json_data['listingAttributes']['page']}.json"
        print(file_name)

            # Ensure the 'results' directory exists
        os.makedirs('results6', exist_ok=True)

        # Define the file path within the 'results' directory
        file_path = os.path.join('results6', file_name)

        # Open the file in the specified path and write to it
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=2)


        # with open(f"{file_name}", 'w', encoding='utf-8') as json_file:
            # json.dump(json_data, json_file, ensure_ascii=False, indent=2)

    print(json_data)
    # time.sleep(30)
