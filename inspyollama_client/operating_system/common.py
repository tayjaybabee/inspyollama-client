import os
from inspyollama_client.operating_system import MOD_LOGGER as PARENT_LOGGER

MOD_LOGGER = PARENT_LOGGER.get_child('common')


def is_windows() -> bool:
    """
    Determine if the operating system is Windows.

    Note:
        - This function is not supported on Linux.
        - This function is not supported on macOS.
        - This function works by checking the `os.name` attribute.

    Returns:
        bool:
            True if the operating system is Windows; False otherwise.
    """
    return os.name == 'nt'


def is_linux() -> bool:
    """
    Determine if the operating system is Linux.

    Note:
        - This function is not supported on Windows.
        - This function is not supported on macOS.
        - This function works by checking the `os.name` and `os.uname().sysname` attributes.

    Returns:
        bool:
            True if the operating system is Linux; False otherwise.
    """
    return os.name == 'posix' and os.uname().sysname == 'Linux'


def is_mac() -> bool:
    """
    Determine if the operating system is macOS.

    Note:
        - This function is not supported on Windows.
        - This function is not supported on Linux.
        - This function works by checking the `os.name` and `os.uname().sysname` attributes.

    Returns:
        bool:
            True if the operating system is macOS; False otherwise.
    """
    return os.name == 'posix' and os.uname().sysname == 'Darwin'


__all__ = [
    'is_windows',
    'is_linux',
    'is_mac',
]
