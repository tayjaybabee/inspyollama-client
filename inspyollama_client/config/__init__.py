from inspyollama_client.config.dirs import DEFAULT_CONFIG_DIR, DEFAULT_CONFIG_FILE_PATH, CONFIG_FILE_NAME
from inspyollama_client.cli.arguments import ARGUMENTS
from typing import Union
from pathlib import Path

from configparser import ConfigParser


class Config:
    DEFAULT_FILE_PATH = DEFAULT_CONFIG_FILE_PATH
    EXAMPLE_CONFIG_FILE_PATH = Path(__file__).parent.joinpath('./example_config.ini')
    __config = ConfigParser()

    def __init__(self, config_file_path=None, ensure_exists=False, non_persist_args=False):
        self.__config_file_path = None
        self.__ensure_exists = ensure_exists

        if config_file_path:
            self.config_file_path = config_file_path

        if not self.config_file_path.exists():
            self.create_config()
        else:
            self.load_config()

        if not non_persist_args:
            self.persist_args(ARGUMENTS)


    @property
    def config_file_path(self):
        return self.__config_file_path or ARGUMENTS.config_file or DEFAULT_CONFIG_FILE_PATH

    @config_file_path.setter
    def config_file_path(self, new: Union[Path, str]):
        if isinstance(new, str):
            new = Path(new)

        if not new.exists():
            raise FileNotFoundError(f'Config file not found: {new}')

        self.__config_file_path = new
        self.load_config()

    @property
    def config(self):
        return self.__config

    def create_config(self):

        self.load_default()
        self.save_config()

    def ensure_config_exists(self):
        if not self.config_file_path.exists():
            if not self.config_file_path.parent.exists():
                self.config_file_path.parent.mkdir(parents=True)
            self.config_file_path.touch()

    def load_config(self):
        self.config.read(self.config_file_path)

    def load_default(self):
        self.config.read(self.EXAMPLE_CONFIG_FILE_PATH)

    def persist_args(self, args):
        for key, value in vars(args).items():
            if key not in ['query', 'config_file']:
                if value is not None:
                    self.config['USER'][key] = str(value)
    def save_config(self):
        with open(self.config_file_path, 'w') as config_file:
            self.config.write(config_file)


CONFIG = Config()
