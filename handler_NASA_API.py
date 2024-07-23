import requests
import json

API_KEY = 'yDf0pzhehgEcpalmhkRbaeNeo6CeWUeWSfB4QWRf'
APOD_URL = 'https://api.nasa.gov/planetary/apod?api_key=' + API_KEY


def save_to_json(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return {
        'title': data.get('title', ''),
        'description': data.get('explanation', ''),
        'image': data.get('url', '')
    }


def process_data(response_text):
    data_dict = json.loads(response_text)
    processed_data = {}
    for key, value in data_dict.items():
        print(f"{key}:")
        print(f"    {value}")
        print("-" * 50)
        processed_data[key] = value
    return processed_data


date_user_input = input("Please enter a date in YYYY-MM-DD format (or leave blank for today's picture): ")
url = APOD_URL
if date_user_input:
    url += f"&date={date_user_input}"

data = fetch_data(url)
print(data)
