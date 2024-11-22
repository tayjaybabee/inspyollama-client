from inspyollama_client.log_engine import ROOT_LOGGER

MOD_LOGGER = ROOT_LOGGER.get_child('operating_system')

# Finish imports for submodules
from inspyollama_client.operating_system.common import *
