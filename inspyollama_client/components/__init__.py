from inspyollama_client.log_engine import ROOT_LOGGER as PARENT_LOGGER

MOD_LOGGER = PARENT_LOGGER.get_child('components')

from inspyollama_client.components.image import Image
