import requests
API_KEY = "aKj6UdWRF25p"

def send_WA(phone_number, message, url_image):
    try:
        url_get = f"http://api.textmebot.com/send.php?recipient={phone_number}&apikey={API_KEY}&text={message}&file={url_image}"
        response_get = requests.get(url_get)
        if response_get.status_code == requests.codes.ok:
            print("ok")
            return response_get.text
        else:
            return response_get.text
    except Exception as e:
        return "Connection Error!"