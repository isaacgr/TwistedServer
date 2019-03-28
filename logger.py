from functools import wraps
import logging

# CRITICAL	50
# ERROR	    40
# ARNING	    30
# INFO	    20
# DEBUG	    10
# NOTSET  	0

class Logger(object):
    """
    Logging decorator.
    """
    def __init__(self, func, message=None):
        self.func = func
        self.message = message
        logging.basicConfig(filename='webserver.log', level=logging.INFO)

    def __call__(self, func):
        """
        If there are decorator arguments, __call__ is
        only called once as a part of the proces. It can only be
        given the function object as a statement
        """
        def wrapper(*args, **kwargs):
            logging.info('{}.'.format(self.message))
        return wrapper
