from color_logging import ColoramaFormatter
import logging
from pathlib import Path
import os

_CONSOLE_FMT = '[{levelname:<8}] {name} : {funcName} {FORE_LIGHTBLACK_EX}->{STYLE_RESET_ALL} {message}'
_FILE_FMT = '{asctime} [{levelname:<8}] {name} : {funcName} : {message}'
_LOGS_FOLDER = Path(os.getcwd()).parent.joinpath('.logs/')
if not _LOGS_FOLDER.exists():
    os.makedirs(_LOGS_FOLDER)


# ======= SETUP LOGGING =======
# Stream handler
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
sh.setFormatter(ColoramaFormatter(
    _CONSOLE_FMT,
    style='{',
    color_config={
        logging.INFO: {
            'levelname': 'FORE_CYAN',
            'name': 'FORE_CYAN,STYLE_DIM',
            'funcName': 'FORE_CYAN,STYLE_DIM'
        },
        logging.WARNING: {
            'levelname': 'FORE_YELLOW',
            'name': 'FORE_YELLOW,STYLE_DIM',
            'funcName': 'FORE_YELLOW,STYLE_DIM'
        },
        logging.ERROR: {
            'levelname': 'FORE_RED',
            'name': 'FORE_RED,STYLE_DIM',
            'funcName': 'FORE_RED,STYLE_DIM'
        },
        logging.CRITICAL: {
            'levelname': 'BACK_RED,STYLE_BRIGHT',
            'name': 'BACK_RED,STYLE_DIM,STYLE_BRIGHT',
            'funcName': 'BACK_RED,STYLE_DIM,STYLE_BRIGHT'
        }
    }
))

# Root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(sh)
fh = logging.FileHandler(_LOGS_FOLDER.joinpath('spam.log'), 'w')
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter(_FILE_FMT, style='{'))
root_logger.addHandler(fh)

# File logger
log = logging.getLogger('toolorant')
log.setLevel(logging.WARNING)
fh = logging.FileHandler(_LOGS_FOLDER.joinpath('toolorant.log'), 'w')
fh.setFormatter(logging.Formatter(_FILE_FMT, style='{'))
log.addHandler(fh)


def main():
    log.debug('This is a {FORE_GREEN}debug message')
    log.info('This is a {FORE_MAGENTA}info message')
    log.warning('This is a warning! {BACK_WHITE}{FORE_BLACK}important information{STYLE_RESET_ALL} occurred')
    log.error('This is a normal error message')
    log.critical('This is a {BACK_GREEN}{STYLE_BRIGHT}critical{BACK_RESET} message')
    print('=========================================================')
    root_logger.debug('Using the root logger to show this {FORE_GREEN}debug message')
    root_logger.info('Using the root logger to show this {FORE_MAGENTA}info message')
    root_logger.warning('Using the root logger {BACK_WHITE}to show this warning! {FORE_BLACK}important information{STYLE_RESET_ALL} occurred')
    root_logger.error('Using the root logger to show this normal error message')
    root_logger.critical('Using the root {STYLE_BRIGHT}logger to show this {BACK_GREEN}critical{BACK_RESET} message')
    return


if __name__ == '__main__':
    main()