import requests

API_KEY = 'yDf0pzhehgEcpalmhkRbaeNeo6CeWUeWSfB4QWRf'
APOD_URL = 'https://api.nasa.gov/planetary/apod?api_key=' + API_KEY


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
if date_user_input:
    url += f"&date={date_user_input}"

data = get_nasa_data(date_user_input)
print(data)
