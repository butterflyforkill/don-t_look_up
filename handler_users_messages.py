# handle users answers
# subscribe of the user
# unsubscribe of the user
# sending the SMS to the user

import requests
from datetime import date
from dateutil import parser


APP_NAME = "DONT_LOOK_UP"


def response_handler(response):
    if response == 200:
        print("message has been sent")
    else:
        print("message hasn't been sent")
    


def get_messages():
    response = requests.get("http://hackathons.masterschool.com:3030/team/getMessages/DONT_LOOK_UP")
    return response.json()


def handle_response_data():
    messages = get_messages()
    today = date.today().isoformat()
    for message in messages:
        for number, data in message.items():
            for item in data:
                date_split = item['receivedAt'].split('T')
                receive_date = date_split[0]
                today = date.today().isoformat()
                if receive_date == today:
                    response_handler(send_message(number))
                

def send_message(user_number):
    message = "Hello, here is the news for today + "# call the method to get data from the json of NASA API
    data = {
        "phoneNumber": user_number,
        "message": message,
        "sender": APP_NAME
    }
    response = requests.post('http://hackathons.masterschool.com:3030/sms/send', json=data) 
    return response.status_code

handle_response_data()
