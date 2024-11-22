from ollama import Client
from inspyollama_client.helpers import TimedText
from yaspin import yaspin
from yaspin.spinners import Spinners
from threading import Thread
from time import sleep
from time import time
from dataclasses import dataclass
import io
import base64
from PIL import Image
from inspyre_toolbox.path_man import provision_path
from pathlib import Path

from inspyollama_client.log_engine import ROOT_LOGGER as PARENT_LOGGER, Loggable


MOD_LOGGER = PARENT_LOGGER.get_child('client')


class Message:
    DEFAULT_PROMPT = 'Are you a large language model?'
    DEFAULT_ROLE   = 'user'
    DEFAULT_PAYLOAD_TEMPLATE = {
        'role': 'user',
        'content': '',
    }


    def __init__(self, message_text=DEFAULT_PROMPT, role=DEFAULT_ROLE):

        # Placeholder for the payload
        self.__payload = None

        # Placeholders for the fields to fill the payload.
        self._content = None
        self._role    = None

        # Placeholder for information about the message itself.
        self._sent    = False

        # Check if there's a message, and if it's not the default prompt, set it.
        if message_text and message_text != self.DEFAULT_PROMPT:
            self.content = message_text

    @property
    def content(self):
        # If the content is not set, return the default prompt.
        return self.DEFAULT_PROMPT if self._content is None else self._content

    @content.setter
    def content(self, new):

        if self._content and self._content != self.DEFAULT_PROMPT:
            raise ValueError(f'Content already set: {self._content}')

        if not isinstance(new, str):
            raise TypeError(f'Content must be a string: {new} ({type(new)})')

    @property
    def payload(self):

        if not self.__payload:
            self.__payload = self.DEFAULT_PAYLOAD_TEMPLATE.copy()
            self.__payload['role'] = self._role
            self.__payload['content'] = self._content

        return self.__payload

    def __dict__(self):
        return self.payload


class ImageMessage(Message):
    DEFAULT_PROMPT = 'Describe this image:'
    OWN_FIELDS = {
        'images': []
    }

    def __init__(self, image_paths, **kwargs):
        super().__init__(**kwargs)
        self.__image_paths      = []
        self.__processed_images = []

    @property
    def image_paths(self):
        return self.__image_paths

    @property
    def processed_images(self):
        return self.__processed_images

    def add_image(self, image_path):
        pass

    def process_images(self):
        pass



    def __dict__(self):
        return super().__dict__().update()



class History:
    def __init__(self, host, port):
        self.__history = []
        self.__host = host
        self.__port = port

    @property
    def history(self):
        return self.__history

    @dataclass(frozen=True)
    class UserMessage:

        def __init__(self, host, port, message):

        def __post_init__(self):
            self.__host = None

        @property
        def to_host(self) -> str:
            return f'{self.host}:{self.port}'

        @to_host.setter
        def to_host(self, new: str):
            if not isinstance(new, str):
                raise TypeError(f'to_host must be a string: {new} ({type(new)})')

            if ':' in new:
                self.host, self.port = new.split(':')
            self.__host = host
            self.__port = port

    @dataclass(frozen=True)
    class ResponseMessage:
        host: str
        port: int
        response: dict

        @property
        def from_host(self):
            return f'{self.host}:{self.port}'

        @property
        def message(self) -> str:
            return self.response['message']['content']

    def add_user_message(self, message):
        self.history.append(self.UserMessage(self.__host, self.__port, message))

    def add_response_message(self, response):
        self.history.append(self.ResponseMessage(self.__host, self.__port, response))


class LlamaClient(Loggable):
    DEFAULT_HOST = 'localhost'
    DEFAULT_PORT = 11434

    EARTH_SPINNER = Spinners.earth
    DEFAULT_MODEL = 'llama3'

    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT, model=DEFAULT_MODEL, skip_auto_connect=False):
        super().__init__(MOD_LOGGER)
        self.__client               = None

        self.__history              = History(host, port)

        self.__host                 = None
        self.__model                = None
        self.__port                 = None
        self.__result_bucket        = None
        self.__skipped_auto_connect = skip_auto_connect

        self.host  = host
        self.port  = port
        self.model = model

        if not skip_auto_connect:
            self.connect()

    def __clean_classify_list__(self, image_paths):
        return [image for image in image_paths if image is not None]

    @property
    def client(self) -> Client:
        return self.__client

    @client.setter
    def client(self, new: Client):
        if self.__client:
            raise ValueError(f'Client already set: {self.__client}')

        if not isinstance(new, Client):
            raise TypeError(f'Client is not an instance of Client: {new} ({type(new)})')

        self.__client = new

    @property
    def connected(self) -> bool:
        return self.check_connection()

    @property
    def model(self) -> str:
        return self.__model

    @model.setter
    def model(self, new: str):
        if self.__model:
            raise ValueError(f'Model already set: {self.__model}')

        if not isinstance(new, str):
            raise TypeError(f'Model is not a string: {new} ({type(new)})')

        self.__model = new.lower()

    @property
    def history(self) -> History:
        return self.__history

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, new: str):
        if self.__host:
            raise ValueError(f'Host already set: {self.__host}')

        if not isinstance(new, str):
            raise TypeError(f'Host is not a string: {new} ({type(new)})')

        self.__host = new

    @property
    def port(self) -> int:
        return self.__port

    @port.setter
    def port(self, new: int):
        port = new
        if self.__port:
            raise ValueError(f'Port already set: {self.__port}')

        if not isinstance(port, (int, str)):
            raise TypeError(f'Port is not an integer: {port} ({type(port)})')
        elif isinstance(port, str) and port.isdigit():
            port = int(port)

        self.__port = port

    @property
    def result_bucket(self) -> dict:
        return self.__result_bucket

    @property
    def skipped_auto_connect(self) -> bool:
        return self.__skipped_auto_connect

    @staticmethod
    def prepare_message(message):
        return [
            {
                'role': 'user',
                'content': message.strip()
            }
        ]

    def connect(self, skip_connection_check=False):
        log = self.create_logger()

        if not self.client:
            self.client = Client(f'{self.host}:{self.port}')

        if not skip_connection_check and not self.connected:
            log.error('Connection failed')
            return False

        return self.client

    def check_connection(self):
        log = self.create_child_logger()
        if not self.client:
            log.error('Client not set')
            log.info('Either set the `client` property manually or call `connect()`')
            return False

        try:
            res = self.client.ps()
            if res:
                log.info(f'Connected to {self.host}:{self.port}')
            return True
        except Exception as e:
            if e.__class__.__name__ == 'ConnectTimeout':
                log.error(f'Connection timed out: {e}')
                return False
            else:
                log.error(f'Error connecting to {self.host}:{self.port}: {e}')
                raise e from e

    @staticmethod
    def prepare_image_message(image_data):
        return [{
            'role': 'user',
            'content': 'Describe this image:',
            'images': image_data
        }]

    def send_no_stream(self, message):
        print(message)
        self.__result_bucket = self.client.chat(model=self.model, messages=message[0])

    def send_and_receive_no_stream(self, message):
        if not isinstance(message, list):
            message = self.prepare_message(message)

        self.history.add_user_message(message)
        print(message)

        request = Thread(target=self.send_no_stream, args=[message])
        request.start()

        with yaspin(self.EARTH_SPINNER, text=TimedText('Waiting for response...')) as sp:
            while not self.result_bucket:
                sleep(0.1)
            sp.ok('Received response!')

            self.history.add_response_message(self.result_bucket)

        res = self.result_bucket
        self.__result_bucket = None
        return res

    def classify_images(self, image_paths, with_progress=False):
        from inspyollama_client.components.image import Image

        if isinstance(image_paths, str):
            image_paths = [image_paths]

        log = self.create_logger()
        image_data = []
        if with_progress:
            from tqdm import tqdm
            log.debug('Using tqdm for progress bar')
            image_paths = tqdm(image_paths)
        else:
            log.debug('No progress bar requested.')
            image_paths = iter(image_paths)

        for image_path in image_paths:
            image_path = Path(image_path)
            log.debug(f'Loading image: {image_path}')
            image = Image(image_path)
            log.debug(f'Loaded image: {image.file_path}')
            image_data.append(image.data)

        image_data = self.__clean_classify_list__(image_data)
        print(len(image_data))
        if image_data:
            raise RuntimeError(image_data)
        data = [image[1] for image in image_data]
        message = self.prepare_image_message(data)

        return self.send_and_receive_no_stream(message)




#
# def get_client(host, port) -> Client:
#     if not isinstance(host, str):
#         raise TypeError('host must be a string')
#     if not isinstance(port, int):
#         raise TypeError('port must be an integer')
#
#     return Client(f'{host}:{port}')
#
#
# def prepare_message(message):
#     return [
#         {
#             'role': 'user',
#             'content': message.strip()
#         }
#     ]
#
#
# result_bucket = None
#
#
# def send_no_stream(client, message):
#     global result_bucket
#     result_bucket = client.chat(
#         model='llama3',
#         messages=message
#     )
#
#
# def send_and_receive_no_stream(client, message):
#     global result_bucket
#     from time import sleep
#
#     if not isinstance(message, list):
#         message = prepare_message(message)
#
#     request = Thread(target=send_no_stream, args=[client, message])
#
#     request.start()
#     with yaspin(EARTH_SPINNER, text=TimedText('Waiting for response: ')) as sp:
#         while not result_bucket:
#             sleep(0.1)
#             if result_bucket:
#                 sp.ok()
#
#         res = result_bucket
#         result_bucket = None
#         return res, sp
#
#
# def send_and_receive(client, message, model):
#     res = client.chat(
#         model='llama3' or model,
#         stream=True,
#         messages=message)
#
#     response = None
#
#     for chunk in res:
#         print(chunk['message']['content'], end='', flush=True)
#
#
# def send_message(client, message, model=None):
#     message = prepare_message(message)
#     return client.chat()
