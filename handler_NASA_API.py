# module get the data
import requests

def get_nasa_data(date):
    url = f"https://api.nasa.gov/planetary/apod?api_key=WQc73ODNIrkpck8Di2SwNldZfLi2YeAgEEr6qgNC&start_date={date}&end_date={date}"
    response = requests.get(url)
    [data_json] = response.json()
    new_data = {
        'title': data_json['title'],
        'description': data_json['explanation'],
        'image': data_json['url']
    }
    return new_data

# class Nasa_Data:
#     def __init__(self) -> None:
#         self.data = {}


#     def get_pod(self, date):
#         url = f"https://api.nasa.gov/planetary/apod?api_key=WQc73ODNIrkpck8Di2SwNldZfLi2YeAgEEr6qgNC&start_date={date}&end_date={date}"
#         response = requests.get(url)
#         data_json = response.json()
#         self.data = {
#             'title': data_json['title'],
#             'description': data_json['explanation'],
#             'image': data_json['url']
#         }
#         return self.data

# date = '2024-07-23'
# url = f"https://api.nasa.gov/planetary/apod?api_key=WQc73ODNIrkpck8Di2SwNldZfLi2YeAgEEr6qgNC&start_date={date}&end_date={date}"
# response = requests.get(url)
# [data_json] = response.json()
# print(data_json)