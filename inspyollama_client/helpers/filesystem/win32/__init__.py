from inspyollama_client.operating_system import is_windows
from inspyollama_client.helpers.filesystem import MOD_LOGGER as PARENT_LOGGER


if not is_windows():
    raise ImportError('This module is only available on Windows systems.')


MOD_LOGGER = PARENT_LOGGER.get_child('win32')

from inspyollama_client.helpers.filesystem.win32.file_attributes import *
