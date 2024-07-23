# module get the data (write option) (update once a day)
import requests
import json_parcer

def get_nasa_data():
    url = "https://api.nasa.gov/planetary/apod?api_key=WQc73ODNIrkpck8Di2SwNldZfLi2YeAgEEr6qgNC"
    response = requests.get(url)
    data_json = response.json()
    new_data = {
        'title': data_json['title'],
        'description': data_json['explanation'],
        'image': data_json['url']
    }
    return new_data