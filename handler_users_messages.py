import handler_NASA_API
import requests
import json_parcer
import schedule
import time
from datetime import date
from collections import defaultdict


APP_NAME = "NASA"
USER_RECEIVE_MESSAGE = "receive_msg.json"


def response_handler(response):
    """
    Handles the response from the SMS sending function.

    Args:
    - response: The response status code from the SMS sending function.

    Returns:
    - A string indicating whether the message has been successfully sent or not.
    """
    return "message has been sent" if response == 200 else "message hasn't been sent"


def get_messages():
    """
    Retrieves messages from the NASA API endpoint and filters out messages containing 'NASA'.
    Filters out repeated commands from the same number.

    Returns:
    - A list of dictionaries, each containing message details such as number, command, and date.
    """
    received_commands = defaultdict(list)
    response = requests.get("http://hackathons.masterschool.com:3030/team/getMessages/NASA")
    json_data = response.json()
    messages = []
    for message in json_data:
        for number, data in message.items():
            for item in data:
                if 'NASA' in item['text']:
                    receive_date = item['receivedAt'].split('T')[0]
                    if item['text'] not in received_commands[number]:  # Check for repeated commands
                        received_commands[number].append(item['text'])
                        messages.append({
                            'number': number,
                            'command': item['text'],
                            'date': receive_date
                        })
    return messages


def messages_timer():
    """
    Schedules the get_messages function to run every hour and returns the messages.
    """
    # Schedule the job to run get_messages every hour
    schedule.every().hour.do(get_messages)
    
    # Allows the first execution of get_messages
    messages = get_messages()
    
    # Run the scheduled jobs
    while True:
        schedule.run_pending()
        time.sleep(1)
    
        # Return the messages
        return messages


def check_user_receive_message(user_number, date):
    """
    Checks if the user has received a message on a given date.

    Args:
    - user_number: The user's phone number.
    - date: The date to be checked.

    Returns:
    - True if the user has already received a message on the given date, otherwise False.
    """
    users_numbers = json_parcer.load_data(USER_RECEIVE_MESSAGE)
    
    if date in users_numbers:
        if user_number in users_numbers[date]:
            return True  # Message has already been sent to this user on this date
        else:
            users_numbers[date].append(user_number)
    else:
        users_numbers[date] = [user_number]
    
    json_parcer.write_file(USER_RECEIVE_MESSAGE, users_numbers)
    return False  # Message has not been sent to this user on this date


def handle_response_data():
    """
    Handles the response data by processing the messages and sending appropriate commands.

    Returns:
    - A message indicating the status of message processing.
    """
    messages = messages_timer()
    today = date.today().isoformat()
    message_sent_today = False
    for message in messages:
        checked_user = check_user_receive_message(message['number'], today)
        checked_date = message['date'] == today
        if not checked_user or checked_date:
            print(commands_handler(message['command'], message['number'], today))
            # commands_handler(message['command'], message['number'], today)
            message_sent_today = True 
    if message_sent_today:
        return "Messages processed and sent successfully"
    else:
        return "No new messages to process or messages already sent today"


def send_message(user_number, nasa_data_date):
    """
    Sends a message with NASA news to the user's phone number.

    Args:
    - user_number: The user's phone number.
    - nasa_data_date: The date for which NASA data is requested.

    Returns:
    - The status code of the message sending operation.
    """
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
    """
    Sends a message with available commands to the user's phone number.

    Args:
    - user_number: The user's phone number.

    Returns:
    - The status code of the message sending operation.
    """
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


def send_in_user_time(user_time, user_number, nasa_data_date):
    """
    Schedule a message to be sent to the user at the specified time using the provided user number and NASA data date.

    Args:
    - user_time: The time at which the message should be sent (format: "HH:MM").
    - user_number: The user's phone number or contact information.
    - nasa_data_date: The relevant date for NASA data being sent in the message.

    This function schedules the message to be sent at the specified user_time using the user_number and the nasa_data_date provided.

    Example:
    send_in_user_time("13:00", "+1234567890", "2024-07-04")
    This example schedules a message to be sent at 13:00 with the NASA data for July 4th, 2024 to the phone number +1234567890.
    """
    schedule.every().day.at(user_time).do(send_message(user_number, nasa_data_date))

    # Continuously run the scheduler
    while True:
        schedule.run_pending()
        time.sleep(1)


def commands_handler(command, number, today):
    """
    Processes the commands received and triggers the appropriate action.

    Args:
    - command: The command received from the user.
    - number: The user's phone number.
    - today: The current date.

    Returns:
    - A message indicating the status of command handling.
    """
    menu_functionality = {
            'SUBSCRIBE NASA': send_message,
            'NASA POD': send_message
    }
    if command in menu_functionality:
        if command == 'SUBSCRIBE NASA':
            # availble_commands = response_handler(send_message_availble_commands(number))
            # send_msg = response_handler(menu_functionality[command](number, today))
            # return f"first_msg: {availble_commands}, second_msg: {send_msg}"
            return "the message was sent"
        else:
            user_time = command.split()[2] + ':00'
            send_in_user_time(user_time, number, today)
            return "the message was sent"

# testing purpose
print(handle_response_data())
# print(get_messages())
# print(send_message_availble_commands('4917664388873'))
