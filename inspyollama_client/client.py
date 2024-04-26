from ollama import Client
from inspyollama_client.helpers import TimedText
from yaspin import yaspin
from yaspin.spinners import Spinners
from threading import Thread



EARTH_SPINNER = Spinners.earth


def get_client(host, port) -> Client:
    if not isinstance(host, str):
        raise TypeError('host must be a string')
    if not isinstance(port, int):
        raise TypeError('port must be an integer')

    return Client(f'{host}:{port}')


def prepare_message(message):
    return [
        {
            'role': 'user',
            'content': message.strip()
        }
    ]


result_bucket = None


def send_no_stream(client, message):
    global result_bucket
    result_bucket = client.chat(
        model='llama3',
        messages=message
    )



def send_and_receive_no_stream(client, message):
    global result_bucket
    from time import sleep

    if not isinstance(message, list):
        message = prepare_message(message)

    request = Thread(target=send_no_stream, args=[client, message])

    request.start()
    with yaspin(EARTH_SPINNER, text=TimedText('Waiting for response: ')) as sp:
        while not result_bucket:
            sleep(0.1)
            if result_bucket:
                sp.ok()

        res = result_bucket
        result_bucket = None
        return res, sp





def send_and_receive(client, message, model):
    res = client.chat(
        model='llama3' or model,
        stream=True,
        messages=message)

    response = None

    for chunk in res:
        print(chunk['message']['content'], end='', flush=True)




def send_message(client, message, model=None):
    message = prepare_message(message)
    return client.chat()
