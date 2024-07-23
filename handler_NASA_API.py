# module get the data (write option) (update once a day)
import requests
import json_parcer

url = "https://api.nasa.gov/planetary/apod?api_key=WQc73ODNIrkpck8Di2SwNldZfLi2YeAgEEr6qgNC"
response = requests.get(url)
data_json = response.json()
new_data = {
    'title': data_json['title'],
    'description': data_json['explanation'],
    'image': data_json['url']
}
json_parcer.write_file('NASA_data.json', new_data)