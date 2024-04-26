"""


Author: 
    Inspyre Softworks

Project:
    inspyollama-client

File: 
    inspyollama-client/cli/dialogs/__init__.py
 

Description:
    

"""
from prompt_toolkit.shortcuts import input_dialog

class Dialog:

    DEFAULT_PROMPT = 'Ask me a question: '
    DEFAULT_TITLE  = 'inspyOllama Client'
    def __init__(self, prompt=None, title=None, auto_build=True, auto_run=False):
        self.__auto_build = None
        self.__auto_run = None
        self.__built    = False
        self.__dialog   = None
        self.__fired    = False
        self.__title    = self.DEFAULT_TITLE
        self.__prompt   = self.DEFAULT_PROMPT
        self.__response = None

        if prompt is not None:
            self.prompt = prompt

        if title is not None:
            self.title = title

        self.auto_build = auto_build
        self.auto_run = auto_run

    @property
    def auto_build(self):
        return self.__auto_build

    @auto_build.setter
    def auto_build(self, new):
        if self.built:
            raise ValueError('Dialog has already been built.')

        if not isinstance(new, bool):
            raise TypeError('auto_build must be a boolean.')
        old = self.auto_build
        self.__auto_build = new
        if not old and self.auto_build:
            self.build_dialog()

    @property
    def auto_run(self):
        return self.__auto_run

    @auto_run.setter
    def auto_run(self, new):
        if self.fired:
            raise ValueError('Dialog has already been fired.')

        if not isinstance(new, bool):
            raise TypeError('auto_run must be a boolean.')

        old = self.auto_run
        self.__auto_run = new

        if not old and self.auto_run:
            self.run_dialog()


    @property
    def built(self):
        return self.__built

    @property
    def dialog(self):
        return self.__dialog

    @property
    def fired(self):
        return self.__response is not None

    @property
    def prompt(self):
        return self.__prompt

    @prompt.setter
    def prompt(self, new):
        if self.fired:
            raise ValueError('Dialog has already been fired.')

        if self.built:
            raise AttributeError('Dialog has already been built')

        try:
            self.__check_string(new)
        except TypeError as e:
            raise TypeError(f'Prompt must be a string! Error: {e}')
        except ValueError as e:
            raise ValueError(f'Prompt must not be empty! Error: {e}')

        self.__prompt = self.__format_prompt(new)

    @property
    def response(self):
        return self.__response

    @staticmethod
    def __check_string(string):
        if not isinstance(string, str):
            raise TypeError('String must be a string.')

        if len(string) == 0:
            raise ValueError('String must not be empty.')

    @staticmethod
    def __format_prompt(prompt):
        if not prompt.endswith(': '):
            prompt = f'{prompt.strip()}: '

        return prompt

    @property
    def status_dict(self) -> dict:
        return {
            'built': self.built,
            'fired': self.fired,
            'prompt': self.prompt,
            'response': self.response,
            'title': self.title
        }

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, new):
        if self.fired:
            raise ValueError('Dialog has already been fired.')

        try:
            self.__check_string(new)
        except TypeError as e:
            raise TypeError(f'Title must be a string! Error: {e}')
        except ValueError as e:
            raise ValueError(f'Title must not be empty! Error: {e}')

        self.__title = new

    def build_dialog(self, force_rebuild=False):
        if self.built and not force_rebuild:
            raise ValueError('Dialog has already been built.')

        if self.fired:
            addendum = ''

            if force_rebuild:
                addendum  = (' [USE OF FORCE RECOGNIZED] - You cannot rebuild a fired dialog. Use `force_rebuild` on `built`'
                             'dialogs that haven\'t been `fired` yet.')
            raise ValueError(f'Dialog has already been fired.{addendum}')

        self.__dialog = input_dialog(
            title=self.title,
            text=self.prompt,

        )

        self.__built = self.dialog is not None

    def run_dialog(self):
        if not self.built:
            raise ValueError('Dialog has not been built yet.')

        if self.fired:
            raise ValueError('Dialog has already been fired.')

        self.__response = self.dialog.run()
