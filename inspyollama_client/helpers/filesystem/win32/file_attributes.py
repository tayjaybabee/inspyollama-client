from pathlib import Path
from typing import Union
from inspyollama_client.helpers.filesystem.win32 import MOD_LOGGER as PARENT_LOGGER
from inspyre_toolbox.path_man import provision_path


MOD_LOGGER = PARENT_LOGGER.get_child('file_attributes')

import ctypes
from ctypes import wintypes


def file_has_recall_attribute(filepath):
    FILE_ATTRIBUTE_RECALL_ON_DATA_ACCESS = 0x00400000  # Flag for online-only files
    INVALID_FILE_ATTRIBUTES = 0xFFFFFFFF

    GetFileAttributesW = ctypes.windll.kernel32.GetFileAttributesW
    GetFileAttributesW.restype = wintypes.DWORD
    GetFileAttributesW.argtypes = [wintypes.LPCWSTR]

    attrs = GetFileAttributesW(filepath)

    if attrs == INVALID_FILE_ATTRIBUTES:
        raise ctypes.WinError()

    return bool(attrs & FILE_ATTRIBUTE_RECALL_ON_DATA_ACCESS)


__all__ = [
    'file_has_recall_attribute',
]
