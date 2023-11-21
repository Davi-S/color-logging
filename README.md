# Color Logging

This Python module provides an extension to the `logging` module, making it easier to add colored output to your logs. It uses the `colorama` library to support ANSI escape sequences for colored text.

## Installation

You can install this module using `pip` with the following command:

```bash
pip install git+https://github.com/Davi-S/color-logging.git
```

## Usage

To use the `ColoramaFormatter`, you first need to import it into your Python script. Here's a simple example:

```python
from color_logging import ColoramaFormatter
import logging

# Define your log format
console_fmt = '[{levelname:<8}] {name} : {funcName} {FORE_LIGHTBLACK_EX}->{STYLE_RESET_ALL} {message}'

# Set up a stream handler with ColoramaFormatter
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
sh.setFormatter(ColoramaFormatter(console_fmt, style='{'))

# Set up the root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(sh)

# Log some messages
root_logger.debug('This is a {FORE_GREEN}debug message')
root_logger.info('This is an {FORE_MAGENTA}info message')
root_logger.warning('This is a warning! {BACK_WHITE}{FORE_BLACK}Important information{STYLE_RESET_ALL} occurred')
root_logger.error('This is a normal error message')
root_logger.critical('This is a {BACK_RED}{STYLE_BRIGHT}critical{STYLE_RESET_ALL} message')
```

In this example, we create a `ColoramaFormatter` and configure a stream handler with different color configurations for different log levels.

## Color Configuration

The color configuration is a dictionary where each key is a logging level (int), and the values are dictionaries with log record attribute names as keys and color codes as values. There can be multiple color codes separated by commas.

Example color configuration:

```python
{
    logging.DEBUG: {
        'levelname': 'FORE_CYAN',
        'message': 'FORE_GREEN',
    },
    logging.INFO: {
        'levelname': 'FORE_YELLOW',
        'message': 'FORE_YELLOW',
    },
    # ... Add configurations for other log levels
}
```

You can use the special attribute "all" to set the value of all record attributes at once.

**Note:** It is not recommended to use the 'all' attribute together with color placeholders in the formatters or messages.
