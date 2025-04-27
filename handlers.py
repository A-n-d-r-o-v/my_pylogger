import logging
from formatters import CustomFormatter, ColorFormatter


def add_console_handler(logger, log_level):
    """ 
    Add a console handler to a logger.

    Keyword arguments:
    logger -- The logger.
    log_level -- The minimum log level required to log the record to the console.
    """
    fmt_str = '%(name)s - %(levelname)s - %(message)s'

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(ColorFormatter(fmt_str))

    logger.addHandler(console_handler)

def add_file_handler(logger, log_level, log_file):
    """ 
    Add a file handler to a logger. 

    Keyword arguments:
    logger -- The logger.
    log_level -- The minimum log level required to log the record to the file.
    log_file -- The file to which the record is logged.
    """
    fmt_str = '%(asctime)s - %(name)s / %(levelname)s: %(message)s'

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    
    file_handler.setFormatter(CustomFormatter(fmt_str))
    logger.addHandler(file_handler)