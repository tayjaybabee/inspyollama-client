from platformdirs import user_config_path, user_log_path
from pathlib import Path


CONFIG_FILE_NAME = 'config.ini'


DEFAULT_CONFIG_DIR = user_config_path(appname='InSPyOllama-Client', appauthor='Inspyre-Softworks')
DEFAULT_CONFIG_FILE_PATH = Path(f'{DEFAULT_CONFIG_DIR}/{CONFIG_FILE_NAME}')




