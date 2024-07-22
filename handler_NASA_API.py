import requests
import json

API_KEY = 'yDf0pzhehgEcpalmhkRbaeNeo6CeWUeWSfB4QWRf'
APOD_URL = 'https://api.nasa.gov/planetary/apod?api_key=' + API_KEY


def fetch_data(url):
    return requests.get(url)


def check_status(response):
    return response.status_code == 200


def process_data(response_text):
    data_dict = json.loads(response_text)
    for key, value in data_dict.items():
        print(f"{key}:")
        if isinstance(value, str) and '\n' in value: # we use this method to print multiple lines of text
            for line in value.split('\n'):
                print(f"    {line}")
        else:
            print(f"    {value}")
        print("-" * 50)


if __name__ == '__main__':
    date = input("Please enter a date in this format YYYY-MM-DD: ")
    url = APOD_URL
    if date:
        url += f"&date={date}"
    response = fetch_data(url)
    if check_status(response):
        process_data(response.text)
    else:
        print("Failed to fetch data:", response.status_code)


