from pathlib import Path
from inspyollama_client.log_engine import Loggable
from inspyollama_client.components import MOD_LOGGER as PARENT_LOGGER

MOD_LOGGER = PARENT_LOGGER.get_child('image')

from inspyollama_client.helpers.images.attributes import file_has_recall_attribute
from inspyollama_client.helpers.images import load_image
from pypattyrn.behavioral.null import Null
from inspyre_toolbox.path_man import provision_path

if 'file_has_recall_attribute' in globals():
    print('file_has_recall_attribute is available')
else:
    file_has_recall_attribute = Null()


class Image(Loggable):
    CAN_RECALL = file_has_recall_attribute

    def __init__(self, file_path, do_not_autoload=False):
        super().__init__(MOD_LOGGER)
        self.__auto_load = None
        self.__data = None
        self.__file_path = None
        self.__loading = False
        self.__needs_load = False

        self.file_path = file_path

        self.auto_load = not do_not_autoload

        if self.auto_load:
            self.load()

    @property
    def auto_load(self):
        return self.__auto_load

    @auto_load.setter
    def auto_load(self, new):
        if not isinstance(new, bool):
            raise TypeError(f'auto_load must be a boolean, not {type(new)}')

        self.__auto_load = new

        # Only load if auto_load is enabled and the data is not already loaded
        if new and not self.__data and self.file_path:
            self.__needs_load = True

    @property
    def data(self):
        if not self.loading and not self.__data and self.__needs_load:
            self.load()

        return self.__data

    @property
    def file_path(self):
        return self.__file_path

    @file_path.setter
    def file_path(self, new):
        if self.__file_path != new:
            self.__data = None
            self.__needs_load = True

        self.__file_path = new

        if self.auto_load and not self.loading and self.file_path_exists:
            self.load()

    @property
    def file_path_exists(self):

        if not self.file_path:
            self.class_logger.error('No file path provided for image.')
            return False

        if not isinstance(self.file_path, Path):
            self.__file_path = provision_path(self.file_path)

        return self.file_path.exists()

    @property
    def loaded(self):
        return self.__data is not None

    @property
    def loading(self):
        return self.__loading

    def load(self):
        log = self.create_logger()
        if self.__loading:
            log.debug('Already loading, skipping redundant load call.')
            return self.__data

        self.__loading = True
        log.debug(f'Loading image: {self.file_path}')

        if self.loaded:
            self.__loading = False
            return self.data

        if not self.file_path:
            self.__loading = False
            raise RuntimeError('No file path provided for image.')

        if not self.file_path_exists:
            self.__loading = False
            raise FileNotFoundError(f'File not found: {self.file_path}')

        with open(self.file_path, 'rb') as f:
            self.__data = f.read()

        self.__loading = False
        self.__needs_load = False

        return self.__data
