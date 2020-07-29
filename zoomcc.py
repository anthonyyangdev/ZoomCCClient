import speech_recognition as sr
import requests
import sys


def post_session(url: str) -> str:
    response = requests.post('http://localhost:8080/session/create', data={'token': url})
    json_data = response.json()
    return json_data['id']


def get_url_plus(id: str) -> str:
    response = requests.get(f'http://localhost:8080/session/{id}')
    json_data = response.json()
    return json_data['url']


def start(zoom_api_token: str):
    r = sr.Recognizer()
    mic = sr.Microphone()
    session_id = post_session(zoom_api_token)
    while True:
        url = get_url_plus(session_id)
        try:
            with mic as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
            message = "Anthony: " + r.recognize_google(audio) + "\n"
            print(message)
            headers = {'content-type': 'text/plain', 'content-length': str(len(message)), 'accept': '*/*'}
            x = requests.post(url, data=message, headers=headers)
            print(x.text)
        except sr.UnknownValueError:
            print("Something odd happened with your speech")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please have the Zoom API token as an argument.")
    else:
        start(sys.argv[1])
