import requests
import json_parcer
import handler_NASA_API
from datetime import date, time


APP_NAME = "DONT_LOOK_UP"
NASA_DATA = "NASA_data.json"
USER_RECEIVE_MESSAGE = "receive_msg.json"


def response_handler(response):
    if response == 200:
        return "message has been sent"
    else:
        return "message hasn't been sent"


def get_messages():
    response = requests.get("http://hackathons.masterschool.com:3030/team/getMessages/NASA")
    json_data = response.json()
    messages = []
    for message in json_data:
        for number, data in message.items():
            for item in data:
                if 'NASA' in item['text']:
                    receive_date = item['receivedAt'].split('T')[0]
                    messages.append({
                        'number': number,
                        'command': item['text'],
                        'date': receive_date
                    })
    return messages


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
        if message['date'] == today and not check_user_receive_message(message['number'], today):
            return commands_handler(message['command'], message['number'], today)
        # else:
        #     return response_handler(commands_handler(message['command'], message['number']))
    return "Message has already been sent today"


def send_message(user_number, nasa_data_date):
    message_data = handler_NASA_API.get_nasa_data(nasa_data_date)
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


def send_message_availble_commands(user_number):
    message = ''
    message += f"Hello dear user of the app Don't Look Up. " 
    message += f"If you want to receive news from us in the different time of the day. Please send us a message with words:"
    message += f" NASA POD and the time u want to receive news.\n"
    message += f"For example: NASA POD 13"  
    data = {
        "phoneNumber": user_number,
        "message": message,
        "sender": APP_NAME
    }
    response = requests.post('http://hackathons.masterschool.com:3030/sms/send', json=data) 
    return response.status_code

def commands_handler(command, number, today):
    menu_functionality = {
            'SUBSCRIBE NASA': send_message,
            'NASA POD': send_message
    }
    if command in menu_functionality:
        if command == 'SUBSCRIBE NASA':
            availble_commands = response_handler(send_message_availble_commands(number))
            send_msg = response_handler(menu_functionality[command](number, today))
            return f"first_msg: {availble_commands}, second_msg: {send_msg}"
        else:
            return response_handler(menu_functionality[command](number, today))
    






print(handle_response_data())
#print(get_messages())
