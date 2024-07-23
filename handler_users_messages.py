import requests
import json_parcer
from datetime import date


APP_NAME = "DONT_LOOK_UP"
NASA_DATA = "NASA_data.json"
USER_RECEIVE_MESSAGE = "receive_msg.json"


def response_handler(response):
    if response == 200:
        return "message has been sent"
    else:
        return "message hasn't been sent"


def get_messages():
    response = requests.get("http://hackathons.masterschool.com:3030/team/getMessages/DONT_LOOK_UP")
    json_data = response.json()
    return json_data


def check_user_receive_message(user_number, date):
    users_numbers = json_parcer.load_data(USER_RECEIVE_MESSAGE)
    if users_numbers.get('date') != date:
        users_numbers = {'date': date, 'numbers': [user_number]}
        json_parcer.write_file(USER_RECEIVE_MESSAGE, users_numbers)
        return False
    elif user_number in users_numbers.get('numbers', []):
        return True
    else:
        numbers = users_numbers['numbers']
        numbers.append(user_number)
        users_numbers['numbers'] = numbers
        json_parcer.write_file(USER_RECEIVE_MESSAGE, users_numbers)
        return False


def handle_response_data():
    messages = get_messages()
    today = date.today().isoformat()
    for message in messages:
        for number, data in message.items():
            for item in data:
                receive_date = item['receivedAt'].split('T')[0]
                if receive_date == today and not check_user_receive_message(number, today):
                    return response_handler(send_message(number))
                elif item['text'] == "SUBSCRIBE DONT_LOOK_UP/n/n":
                    return response_handler(send_message(number))
        return "Message has already been sent today"


def send_message(user_number):
    message_data = json_parcer.load_data(NASA_DATA)
    title = message_data['title']
    explanation = message_data['description'].split('.')
    image = message_data['image']
    message = f"Hello, dear user. \nToday news is about {title}. \n {explanation[0]}. {explanation[1]}.\n {image}"# call the method to get data from the json of NASA API
    data = {
        "phoneNumber": user_number,
        "message": message,
        "sender": APP_NAME
    }
    response = requests.post('http://hackathons.masterschool.com:3030/sms/send', json=data) 
    return response.status_code

print(handle_response_data())
# print(get_messages())
