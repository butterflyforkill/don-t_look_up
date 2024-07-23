# handle users answers
# subscribe of the user
# unsubscribe of the user
# sending the SMS to the user

import requests
from datetime import date
from dateutil import parser

APP_NAME = "DONT_LOOK_UP"


def response_handler(response):
    """
    Prints a message indicating whether a message has been sent successfully based on the response code.

    Parameters:
    - response (int): The HTTP status code returned by a request.

    Returns:
    None
    """
    if response == 200:
        print("message has been sent")
    else:
        print("message hasn't been sent")


def get_messages():
    """
    Fetches messages for the application from a predefined URL.

    Returns:
    - json: A JSON object containing the fetched messages.
    """
    response = requests.get("http://hackathons.masterschool.com:3030/team/getMessages/DONT_LOOK_UP")
    return response.json()


def handle_response_data():
    """
    Processes the fetched messages, filtering them by the current date and sending a message to each user.

    Iterates through each message, checks if the message was received today, and if so, sends a message to the user.

    Returns:
    None
    """
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
    """
    Sends a message to a specified user number.

    Constructs a message and sends it to the user using a predefined URL.

    Parameters:
    - user_number (str): The phone number of the user to whom the message will be sent.

    Returns:
    - int: The HTTP status code returned by the post request.
    """
    message = "Hello, here is the news for today + "  # call the method to get data from the json of NASA API
    data = {
        "phoneNumber": user_number,
        "message": message,
        "sender": APP_NAME
    }
    response = requests.post('http://hackathons.masterschool.com:3030/sms/send', json=data)
    return response.status_code


handle_response_data()