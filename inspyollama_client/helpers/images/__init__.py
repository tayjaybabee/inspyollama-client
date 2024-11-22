from PIL import Image
import io
import base64
from inspyre_toolbox.path_man import provision_path
from pathlib import Path
from typing import Union
from inspyollama_client.helpers import MOD_LOGGER as PARENT_LOGGER
from inspyollama_client.helpers.filesystem.win32.file_attributes import file_has_recall_attribute


MOD_LOGGER = PARENT_LOGGER.get_child('images')


def prepare_image_path(image_path, do_not_provision=False, raise_error_if_not_existant=False):
    if not do_not_provision:
        image_path = provision_path(image_path)

    if not isinstance(image_path, Path):
        raise TypeError('Image path must be a Path object!')

    if not image_path.exists():
        if not raise_error_if_not_existant:
            return None
        else:
            raise FileNotFoundError(f'Image path {image_path} not found!')

    return image_path


def load_image(image_path: Union[str, Path],  do_not_provision=False, fetch_from_one_drive=False):
    image_path = prepare_image_path(image_path, do_not_provision=do_not_provision)
    if file_has_recall_attribute(str(image_path)) and not fetch_from_one_drive:
        return image_path, None

    try:
        with Image.open(image_path) as img:
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG')
            img_bytes = img_byte_arr.getvalue()
    except OSError as e:
        MOD_LOGGER.error(f'Cannot open image: {image_path}')
        return None, None

    return (image_path, base64.b64encode(img_bytes).decode('utf-8'))


def load_images(image_paths: list[Path], do_not_provision=False, calculate_hashes=False):
    """
    Loads a list of image paths into a list of base64 encoded images.

    Parameters
    ----------
    image_paths : list[Path]
        The paths to the images to be loaded.
    do_not_provision : bool, optional
        If True, the image paths are not provisioned. Defaults to False.
    calculate_hashes : bool, optional
        If True, the MD5 hashes of the images are calculated. Defaults to False.

    Returns
    -------
    list[str]
        A list of base64 encoded images.
    """
    new_image_paths = []
    if not do_not_provision:

        for image_path in image_paths:
            new_image_paths.append(prepare_image_path(image_path))

    else:
        new_image_paths = [Path(image_path) for image_path in image_paths]

    return [load_image(image_path, True)[1] for image_path in new_image_paths]
