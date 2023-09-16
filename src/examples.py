import logging
import custom_logging as c_log

# ======= SETUP LOGGING =======
# Stream handler
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
# Set the colorama formatter on the stream handler to see colors on the terminal
sh.setFormatter(c_log.ColoramaFormatter(
    # Using a simple formatter string for the terminal
    c_log.formatters[0],
    style='{',
    # Set colors to use in each logging level
    color_config={
        logging.INFO: {
            'levelname': 'FORE_CYAN',
            'name': 'FORE_CYAN'
        },
        logging.WARNING: {
            'levelname': 'FORE_YELLOW',
            'name': 'FORE_YELLOW',
        },
        logging.ERROR: {
            # Any extra color placeholders on the format string will 'cut' the 'all' attribute
            'all': 'FORE_RED',
        },
        logging.CRITICAL: {
            'levelname': 'BACK_RED,STYLE_BRIGHT',
        }
    }
))

# Configure root logger
root_logger = logging.getLogger()
# Set debug level on the root logger to get every log record (you can set a higher level on the handlers or child loggers depending on your needs)
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(sh)
# Using the create_file_handler function to create the file with the logs folder path
fh = c_log.create_file_handler('spam', 'w')
fh.setLevel(logging.DEBUG)
# Using default formatter for file handlers to not show scape characters (color codes) on the file
fh.setFormatter(logging.Formatter(c_log.formatters[1], style='{'))
root_logger.addHandler(fh)

# Configure file logger
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
fh = c_log.create_file_handler(__name__, 'w')
fh.setFormatter(logging.Formatter(c_log.formatters[1], style='{'))
log.addHandler(fh)


def main():
    # Note that some records will not be printed on the console because of the levels
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