# handle users answers
# subscribe of the user
# unsubscribe of the user
# sending the SMS to the user

import requests


def response_handler(response):
    pass


def get_messages():
    response = requests.get("http://hackathons.masterschool.com:3030/team/getMessages/DONT_LOOK_UP")
    return response_handler(response)

def handle_response_data():
    number, messages = get_messages()
    for i in range(len(messages)):
        date = messages[i]['receivedAt']
        pass

def send_message(user_number):
    message = # call the method to get data from the json or NASA API
    data = {
        "phoneNumber": user_number,
        "message": message,
        "sender": "DONT_LOOK_UP"
    }
    response = requests.post('http://hackathons.masterschool.com:3030/sms/send', json=data) 
    return response_handler(response)



# response = requests.get("http://hackathons.masterschool.com:3030/team/getMessages/DONT_LOOK_UP")
# print(response.text)