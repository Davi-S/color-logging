# THIS IS THE MAIN FILE, MEANT TO BE RUN
# First of all, setup logging configuration. This is only needed on the main file. Will affect all other log instances in other files
import logging
import logging.config
from logging_configuration import CONFIG_DICT, create_file_handler
logging.config.dictConfig(CONFIG_DICT)

# IMPORTS #
import helpers


# Get the file logger and its handler
log = logging.getLogger(__name__)
log.addHandler(create_file_handler(__name__))


def main():
    return


if __name__ == '__main__':
    main()