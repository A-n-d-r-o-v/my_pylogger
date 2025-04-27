import logging
from contextlib import contextmanager

from config import DEFAULT_SETTINGS
from handlers import add_console_handler, add_file_handler
from custom_logger import CustomLogger


def create_logger(name, 
                  log_file="log.log", 
                  console_log_level=logging.WARNING, 
                  file_log_level=logging.DEBUG,
                  settings: dict = None
) -> logging.Logger:
    """ 
    Create and return a logger.

    name -- the name of the logger
    log_file -- the file to which the log is written (default: "log.log")
    console_log_level -- the log level required to write to the console (default: warning)
    file_log_level -- the log level required to write to the log file (default: debug)
    settings -- custom logger settings.
    """

    log_settings = DEFAULT_SETTINGS.copy()
    if settings:
        # Any settings that are in custom_settings but do not exist in default_settings
        unknown_settings = set(settings) - set(DEFAULT_SETTINGS)
        if unknown_settings:
            raise KeyError(f"Unknown setting(s): {unknown_settings}")
        log_settings.update(settings)

    logging.setLoggerClass(CustomLogger)
    logger = logging.getLogger(name)

    logger._settings = log_settings

    # Force console & file log levels to DEBUG if applicable
    if name in log_settings["DEBUG_OVERRIDES"]:
        console_log_level = logging.DEBUG
        file_log_level = logging.DEBUG

    if not logger.handlers:
        add_console_handler(logger, console_log_level)
        add_file_handler(logger, file_log_level, log_file)

        logger.setLevel(min(console_log_level, file_log_level))

    #if _LOG_FILE_NAME_AND_LINE_NO:
    #    for handler in logger.handlers:
    #        handler.formatter.format.__format__ += ' [%(module)s: %(lineno)d]'

    if log_settings["LOG_ON_CREATE"]:
        logger.debug(f"Logger created.", extra={"simple_formatting": True, "settings": log_settings})

    return logger


@contextmanager
def temp_settings(logger: logging.Logger, **overrides):
    """ Temporarily set logger to level (e.g with "with" keyword), then restore. """
    old = {k: logger._settings[k] for k in overrides}

    logger._settings.update(overrides)
    try:
        yield
    finally:
        logger._settings.update(old)


# ---------------------------------

def example_usage():
    _logger = create_logger("test log", log_file="test_log.log", console_log_level=logging.DEBUG)
    _logger.info("Hello world")
    _logger.info("Hello sir")

    for _ in range(100):
        _logger.info("Hello world a lot", suppress_duplicates=True)

    _logger.critical("Hello world a lot", suppress_duplicates=True)
    _logger.info("Hello world twice")
    _logger.info("Hello world")

    some_var = 42
    _logger.info(f"Highlight the variable color for {some_var=} (default behaviour)", highlight=True)
    _logger.info(f"Do NOT highlight the variable color for {some_var=}", highlight=False)

    _logger.warning("Hello world")
    _logger.warning("Hello warning", extra={'simple_formatting': True}) # Log in file with simple formatting

    _logger.error("Oh no, that's bad!")

    _logger2 = create_logger("test log 2", log_file="test_log2.log", console_log_level=logging.DEBUG, settings={"LOG_DEBUG_FORMAT_EXTRAS": True, "DEBUG_FORMAT_EXTRAS": ['%(funcName)s', '%(filename)s', '%(lineno)d']})
    _logger2.warning("Hello warning")
    _logger2.warning("Hello world")

    _logger2.critical("Critical!!")

    # Temporary log level
    with temp_settings(_logger, LOG_DEBUG_FORMAT_EXTRAS=True):
        _logger.info("Calling log with some temporary settings")
        _logger.critical("Again calling log with some temp settings")

    _logger.info("Now we are back to the normal settings")


def example_usage_sfm_BA():
    _log = create_logger("BA", log_file="BA.log")

    img_id = 42
    _log.info(f"Starting bundle adjustments on img {img_id=}")
    _log.warning("Sub-optimal amt of points or something")
    _log.info("Step 1 done")
    n_pts = 123
    _log.debug(f"{n_pts=}")

    _log.error("BA optimization step failed. Continuing without optimization...")
    _log.critical("Failed to perform bundle adjustment! Terminating...")

def example_usage_fm_dense():
    _log = create_logger("densification", log_file="densification.log")

    n_pts_sparse = 357
    n_imgs = 14
    _log.info(f"Start densification with {n_imgs=}")
    _log.debug(f"Num points before densification: {n_pts_sparse=}")


# Test / example usage.
if __name__ == "__main__":
    example_usage_sfm_BA()
    example_usage_fm_dense()
    #example_usage()
