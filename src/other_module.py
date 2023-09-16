# THIS FILE CONTAIN GENERIC USEFUL CALLABLES #
# THIS FILE IS JUST AND EXEMPLE; IT IS NOT NEEDED TO LOGGING CONFIGURATION AND SETUP #

# IMPORTS #
from logging_configuration import create_file_handler
import logging

# Get the file logger and its handler
log = logging.getLogger(__name__)
log.addHandler(create_file_handler(__name__))


# Singleton metaclass for creating sigleton classes
class Singleton(type):
    _instances = {}
    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            self._instances[self] = super(Singleton, self).__call__(*args, **kwargs)
        return self._instances[self]


# Base class to implement post_init equivalent method of dataclasses in normal classes
class PostInit:
    def __init_subclass__(cls, **kwargs):
        def init_decorator(previous_init):
            def new_init(self, *args, **kwargs):
                previous_init(self, *args, **kwargs)
                if type(self) == cls:
                    self.__post_init__()
            return new_init

        cls.__init__ = init_decorator(cls.__init__)

    def __post_init__(self):
        pass
    

def list_intersection(list_1, list_2):
    """Return the intersection of two lists"""
    return [value for value in list_1 if value in list_2]


def remove_sublist(main_list, sub_list):
    """Remove a sub list from a list"""
    return list(set(main_list) - set(sub_list))
