import speech_recognition as sr
import requests


def post_session(url: str) -> str:
    print("Making post request")
    response = requests.post('https://zoomcc.herokuapp.com/session/create', data={'token': url})
    json_data = response.json()
    print("Received id")
    return json_data['id']


def get_url_plus(id: str) -> str:
    print("Making get request")
    response = requests.get(f'https://zoomcc.herokuapp.com/session/{id}')
    json_data = response.json()
    print("Received url")
    return json_data['url']


def start(name: str, zoom_api_token: str):
    r = sr.Recognizer()
    mic = sr.Microphone()
    session_id = post_session(zoom_api_token)
    while True:
        url = get_url_plus(session_id)
        try:
            with mic as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
            message = f"{name}: " + r.recognize_google(audio) + "\n"
            print(message)
            headers = {'content-type': 'text/plain', 'content-length': str(len(message)), 'accept': '*/*'}
            x = requests.post(url, data=message, headers=headers)
            print(x.text)
        except sr.UnknownValueError:
            print("Something odd happened with your speech")


if __name__ == "__main__":
    print("Input your display name:")
    name_input = input(">>").strip()
    if name_input == 'cancel':
        exit(0)
    print("")
    print("Paste the Zoom API token")
    print("(This is obtained by clicking on 'Closed Captions' at the bottom, and selecting 'Copy the API token')")
    usr_input = input(">>").strip()
    if usr_input == 'cancel':
        exit(0)
    start(name_input, usr_input)
