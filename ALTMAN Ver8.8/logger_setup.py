import logging
import os
import sys

import tracker_config as tkc


LOG_DIRECTORY = tkc.PRINGLES
# LOG_FILE = 'TESTJAN23MAIN.txt'


log_directory = os.path.join(os.path.expanduser('~'), tkc.PRINGLES)

# Create the directory if it doesn't exist
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Path to your log file
log_file = os.path.join(log_directory, tkc.LOG_FILE)

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt=tkc.DATEFORMAT,
                    filename=log_file,
                    filemode=tkc.FILE_MODE)
