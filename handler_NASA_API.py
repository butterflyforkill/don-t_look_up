import requests
import json

API_KEY = 'yDf0pzhehgEcpalmhkRbaeNeo6CeWUeWSfB4QWRf'
APOD_URL = 'https://api.nasa.gov/planetary/apod?api_key=' + API_KEY


def save_to_json(data, filename='nasa_data.json'):
    """Save the given data to a JSON file."""
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def check_status(response):
    if response.status_code == 200:
        print("Message has been sent.")
        return True
    else:
        print("Message hasn't been sent.")
        return False


def process_data(response_text):
    data_dict = json.loads(response_text)
    processed_data = {}
    for key, value in data_dict.items():
        print(f"{key}:")
        print(f"    {value}")
        print("-" * 50)
        processed_data[key] = value
    return processed_data


def get_nasa_data(date=None):
    url = APOD_URL
    if date:
        url += f"&date={date}"
    
    response = requests.get(url)
    response.raise_for_status()
    data_json = response.json()
    
    return {
        'title': data_json['title'],
        'description': data_json['explanation'],
        'image': data_json['url']
    }


# testing function arena
date_user_input = input("Please enter a date in YYYY-MM-DD format (or leave blank for today's picture): ")
url = APOD_URL

url += f"&date={date_user_input}"

data = get_nasa_data(date_user_input)
save_to_json(data, filename='nasa_data.json')
print("Data saved to nasa_data.json")
