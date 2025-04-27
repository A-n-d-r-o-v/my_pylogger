DEFAULT_SETTINGS = {
    "DISABLE_LOGGING": False, # Disable all logging.
    "LOG_ON_CREATE": True, # Log (at debug level) whenever a new logger is created.
    "DEBUG_OVERRIDES": ["densification"], # Force console and file log level to DEBUG if name is in _ACTIVE_DEBUG_MODULES

    # Debug specifiers are extra logging specifications used when _LOG_DEBUG_FORMAT_EXTRAS 
    # is enabled. If a specifier already exists in the format, it won't be added twice.
    # See https://docs.python.org/3/library/logging.html#logrecord-attributes for a full list.
    "LOG_DEBUG_FORMAT_EXTRAS": False,
    "DEBUG_FORMAT_EXTRAS": ['%(filename)s', '%(lineno)d'],

    # Suppress duplicate logs.
    "ALWAYS_SUPPRESS_DUPLICATES": False, # Always call log(...) with suppress_duplicates=True.
    "LOG_SUPPRESS_COUNT_THRESHOLD": 3, # Number of duplicates until said number is shown.

    "AUTO_HIGHLIGHT_VARS": True # Automatically highlight f"... {var=} ..." occurrences 
}
