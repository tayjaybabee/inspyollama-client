import os
from inspyollama_client.helpers import MOD_LOGGER as PARENT_LOGGER
from inspyollama_client.operating_system.common import is_windows
from typing import Union
from pathlib import Path
from inspyre_toolbox.path_man import provision_path

MOD_LOGGER = PARENT_LOGGER.get_child('filesystem')


MOD_LOGGER.debug('Importing filesystem submodules')

__all__ = []

if is_windows():
    MOD_LOGGER.debug('Detected Windows operating system; importing win32 submodules')
    from inspyollama_client.helpers.filesystem.win32 import *
    __all__.append('file_has_recall_attribute')


def check_path(
        path: Union[str, Path],
        do_not_expand: bool = False,
        do_not_resolve: bool = False,
        do_not_convert: bool = False,
        do_not_provision: bool = False,
) -> bool:
    """
    Check if a path is valid.

    This function checks if a path is valid. If the path is a string, it will be converted to a Path object. If the path
    is not expanded, it will be expanded. If the path is not resolved, it will be resolved. If the path is not converted
    to a string, it will be converted to a string. If the path is not provisioned, it will be provisioned.

    Note:
        Provisioning a path involves converting it to a Path object, expanding it, and resolving it.

    Parameters:
        path (Union[str, Path]):
            The path to check.

        do_not_expand (bool):
            A flag indicating whether to expand the path.

        do_not_resolve (bool):
            A flag indicating whether to resolve the path.

        do_not_convert (bool):
            A flag indicating whether to convert the path to a string.

        do_not_provision (bool):
            A flag indicating whether to provision the path.

    Returns:
        bool:
            A flag indicating whether the path is valid.
    """
    if not do_not_provision:
        path = provision_path(
            path,
            do_not_convert=do_not_convert,
            do_not_expand=do_not_expand,
            do_not_resolve=do_not_resolve
        )

    return path.exists() if isinstance(path, Path) else False


def check_directory(
        path: Union[str, Path],
        **kwargs
) -> bool:
    """
    Check if a directory is valid.

    This function checks if a directory is valid. If the path is a string, it will be converted to a Path object. If the
    path is not expanded, it will be expanded. If the path is not resolved, it will be resolved. If the path is not
    converted to a string, it will be converted to a string. If the path is not provisioned, it will be provisioned.

    Note:
        Provisioning a path involves converting it to a Path object, expanding it, and resolving it.

    Parameters:
        path (Union[str, Path]):
            The directory to check.

        **kwargs:
            Additional keyword arguments.

    Returns:
        bool:
            A flag indicating whether the directory is valid.
    """
    return path.is_dir() if check_path(path, **kwargs) else False


def check_file(
        path: Union[str, Path],
        **kwargs
) -> bool:
    """
    Check if a file is valid.

    Parameters:
        path (Union[str, Path]):
            The file to check.

    Returns:
        bool:
            A flag indicating whether the file is valid.
    """
    return path.is_file() if check_path(path, **kwargs) else False


def gather_files_in_dir(
        directory: Union[str, Path],
        recursive: bool = False,
        file_types: Union[str, list] = None,
        ignore_dirs: list = None,
        ignore_case: bool = False,
        parent_logger=None,
        **kwargs
) -> list:
    """
    Gather all files in a directory.

    Parameters:
        directory (Union[str, Path]):
            The directory to gather files from.

        recursive (bool):
            A flag indicating whether to gather files recursively.

        file_types (Union[str, list]):
            The file types to gather.

        ignore_dirs (list):
            A list of directory names to ignore.

        ignore_case (bool):
            A flag indicating whether to ignore case when matching directory names.

    Returns:
        list:
            A list of files in the directory.
    """
    _name = 'gather_files_in_dir'

    if not MOD_LOGGER.find_child_by_name(_name):
        log = MOD_LOGGER.get_child(_name)
    else:
        log = MOD_LOGGER.find_child_by_name(_name)[0]

    log.debug(f'Gathering files in directory: {directory}')

    log.debug(f'Provisioning directory: {directory}')
    directory = provision_path(directory)

    log.debug(f'Checking if directory exists: {directory}')
    if not check_directory(directory):
        raise FileNotFoundError(f"Directory not found: {directory}")

    if not file_types:
        log.debug('No file types specified. Using wildcard: *')
        file_types = ['*']

    log.debug(f'File types: {file_types}')

    if isinstance(file_types, str):
        log.warning('File types is a string. Converting to list.')
        file_types = [file_types]

    if ignore_dirs is None:
        log.debug('No directories to ignore. Setting empty list')
        ignore_dirs = []

    if ignore_case:
        log.debug('Ignoring case for directory names.')
        ignore_dirs = [dir_name.lower() for dir_name in ignore_dirs]
    else:
        log.debug('Not ignoring case for directory names.')

    files = []
    log.debug('Set up files list. Starting directory walk...')

    for dirpath, dirnames, filenames in os.walk(directory):
        log.debug(f'Checking directory: {dirpath}')
        if ignore_case:
            log.debug('Ignoring case for directory names.')
            dirnames[:] = [d for d in dirnames if d.lower() not in ignore_dirs]
        else:
            log.debug('Not ignoring case for directory names.')
            dirnames[:] = [d for d in dirnames if d not in ignore_dirs]

        if not recursive:
            log.debug('Not gathering files recursively. Clearing directory names list.')
            while len(dirnames) > 0:
                log.debug(f'Popping directory name: {dirnames[-1]}')
                dirnames.pop()
                log.debug(f'Number of directory names left: {len(dirnames)}')

        for file_type in file_types:
            log.debug(f'Gathering files of type: {file_type}')
            files.extend(
                os.path.join(dirpath, filename)
                for filename in filenames
                if filename.endswith(file_type)
            )

    log.debug(f'Files gathered: {files}')
    log.debug(f'Gathered {len(files)} files in directory: {directory} | Recursive: {recursive}')

    return files
