import logging
import os
import re
from pathlib import Path

import colorama


_LOG_FOLDER = Path(os.path.join(os.getcwd(), '.logs'))

# Join all color codes from colorama
_ALL_VALUES = {f'BACK_{key}': value for key, value in colorama.Back.__dict__.items()} | {f'FORE_{key}': value for key, value in colorama.Fore.__dict__.items()} | {f'STYLE_{key}': value for key, value in colorama.Style.__dict__.items()}

# list of formatter strings to keep consistency
formatters = [
    '{levelname:<8} {name} : {funcName} {FORE_LIGHTBLACK_EX}-> {STYLE_RESET_ALL}{message}',
    '{asctime} : {levelname:<8} : {name} : {funcName} : {message}',
]


class Default(dict):
    """Dict that returns a placeholder with the key when trying to format a missing key"""

    def __missing__(self, key):
        return f'%({key})s'


class ColoramaPercentStyle(logging.PercentStyle):
    def __init__(self, fmt, color_config, *, defaults=None):
        self._fmt = self._add_reset_all(fmt) if fmt else self.default_format
        self._defaults = defaults
        self._color_config = color_config

    def _format(self, record):
        values = self._defaults | record.__dict__
        if self._color_config:
            if 'all' in self._color_config[record.levelno]:
                fmt = self.wrap_all(self._fmt, self._color_config[record.levelno])
            else:
                fmt = self.wrap_placeholders(self._fmt, self._color_config[record.levelno])
        return fmt % values

    def _format_message(self, msg):
        return msg % Default(_ALL_VALUES)

    def _add_reset_all(self, fmt):
        # sourcery skip: use-fstring-for-concatenation
        return fmt + '%(STYLE_RESET_ALL)s'

    @staticmethod
    def wrap_placeholders(fmt: str, wrapper_dict: dict[str, str]) -> str:
        # TODO: refactor this function to make it more efficient. It is using several unnecessary regex
        pattern = '|'.join([f'%\({placeholder_name}\)[\w-]*'
                            for placeholder_name in wrapper_dict])
        placeholders = re.findall(pattern, fmt)
        result = fmt
        for placeholder in placeholders:
            placeholder_name = re.match(r'%\((.*?)\)[\w-]*', placeholder)[1]
            prefixes = ''.join(f'%({replace})s'
                               for replace in wrapper_dict[placeholder_name].split(','))
            replacement = f"{prefixes}{placeholder}%(STYLE_RESET_ALL)s"
            result = result.replace(placeholder, replacement)
        return result
    
    @staticmethod
    def wrap_all(fmt: str, wrapper_dict: dict[str, str]) -> str:
        prefixes = ''.join(f'%({value})s'
                           for value in wrapper_dict['all'].split(','))
        return prefixes + fmt


class ColoramaStrFormatStyle(ColoramaPercentStyle, logging.StrFormatStyle):
    def _format(self, record):
        values = self._defaults | record.__dict__
        if self._color_config:
            if 'all' in self._color_config[record.levelno]:
                fmt = self.wrap_all(self._fmt, self._color_config[record.levelno])
            else:
                fmt = self.wrap_placeholders(self._fmt, self._color_config[record.levelno])
        return fmt.format(**values)

    def _format_message(self, msg):
        return msg.format(**_ALL_VALUES)

    def _add_reset_all(self, fmt):
        return fmt + '{STYLE_RESET_ALL}'

    def validate(self):
        logging.StrFormatStyle.validate(self)

    @staticmethod
    def wrap_placeholders(fmt: str, wrapper_dict: dict[str, str]) -> str:
        for key in wrapper_dict:
            placeholder_start = fmt.find('{' + key)
            placeholder = fmt[placeholder_start:fmt.find('}',
                                                         placeholder_start) + 1]
            prefixes = ''.join(f'{{{value}}}'
                               for value in wrapper_dict[key].split(','))
            replacement = f'{prefixes}{placeholder}' + '{STYLE_RESET_ALL}'
            fmt = fmt.replace(placeholder, replacement)
        return fmt

    @staticmethod
    def wrap_all(fmt: str, wrapper_dict: dict[str, str]) -> str:
        prefixes = ''.join(f'{{{value}}}'
                           for value in wrapper_dict['all'].split(','))
        return prefixes + fmt


_COLORAMA_STYLES = {
    '%': ColoramaPercentStyle,
    '{': ColoramaStrFormatStyle
    # TODO: add '$' style
}


class ColoramaFormatter(logging.Formatter):
    # TODO: add support for the '$' style
    """
    A logging formatter with support for color placeholders and color configuration based on the logging level.

    To use colors, just use a placeholder with the color code.
    The color code has the following format: TYPE + _ + COLOR NAME
    where type can be one of: FORE, BACK, STYLE;
    and the color name can be any of the colorama constant shorthand for ANSI escape sequences (https://pypi.org/project/colorama/)
    Example: FORE_RED, STYLE_BRIGHT, ...
    (The color codes are always upper case)

    These color codes can be placed anywhere on the formatter string and on the message.

    The color configuration is a way to configure colors for the log record attributes based on on log level.
    It is a dictionary where each key is the logging level (int) and the values are a dictionary with the log record attributes name as key and the color codes as values. There can be multiple color codes separate by comma and with no space.
    `Dict[logging.level, Dict[logging.record_attribute_name_string, color_code_str]]`
    There is a special attribute called "all" which is used to set the value of all record attributes at once
    Example of a simple color configuration dict:
    {
        logging.DEBUG: {
            'levelname': 'FORE_CYAN,BACK_RED',
            'message': 'FORE_GREEN',
            'name': 'STYLE_BRIGHT',
        },    
        logging.WARNING: {
            'levelname': 'FORE_RED',
            'asctime': 'FORE_RED,BACK_WHITE',
            'module': 'STYLE_BOLD',
        },
        logging.INFO: {
            'all': 'FORE_BLACK,BACK_WHITE'
        }
    }
    It is not recommended to use the 'all' attribute together with color placeholders on the formatters on message
    """

    def __init__(self, fmt=None, datefmt=None, style='%', validate=True, color_config=None, *, defaults=None):
        if style not in logging._STYLES:
            raise ValueError(f"Style must be one of: {','.join(logging._STYLES.keys())}")

        self._style = _COLORAMA_STYLES[style](fmt, color_config,
                                              defaults=(defaults or {}) | _ALL_VALUES)

        if validate:
            self._style.validate()
        self._fmt = self._style._fmt
        self.datefmt = datefmt

    def format(self, record):
        message = super().format(record)
        # Format the color placeholders that are on the message and return.
        return self._style._format_message(message)


def create_file_handler(filename, mode='a', encoding='utf-8', delay=False, errors=None):
    """Create a file handler with the log folder path"""
    file_path = Path(os.path.join(_LOG_FOLDER, f'{filename}.log'))
    return logging.FileHandler(file_path, mode, encoding, delay, errors)
