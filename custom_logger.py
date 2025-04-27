import logging
from dataclasses import dataclass

from config import DEFAULT_SETTINGS
# ---------------------------------

@dataclass
class RecordData:
    """ 
    Helper class to hold log record data. 
    This represents the comparison metric used to check whether or not two records are seen as duplicates.
    """
    name: str
    levelno: int
    msg: str

# ---------------------------------

class CustomLogger(logging.Logger):
    """ 
    Custom logger implementation designed to log records while suppressing duplicate entries.
    """
    def __init__(self, name: str, settings: dict = DEFAULT_SETTINGS) -> None:
        super().__init__(name=name)

        self.settings = settings.copy()

        self.last_log_record_data = None
        self.duplicate_count = 0

    def log(self, level, msg, suppress_duplicates=False, *args, **kwargs):
        """ Call custom log. """

        if self.settings["DISABLE_LOGGING"]:
            return
        if not self.isEnabledFor(level):
            return
        
        # Duplicate log suppression
        record_data = RecordData(self.name, level, msg)
        suppress_logs_enabled = suppress_duplicates or self.settings["ALWAYS_SUPPRESS_DUPLICATES"]
        suppress = self.is_duplicate(record_data) and suppress_logs_enabled

        if not suppress:
            # Log number of previously suppressed logs
            if self._log_suppress_count():
                super().log(logging.DEBUG, f"[Suppressed {self.duplicate_count} duplicate log(s)]", *args,
                    extra={'simple_formatting': True}, **kwargs)

            # Keep track of the last record that was logged
            self.last_log_record_data = record_data 
            self.duplicate_count = 0

            # f-string variable highlight 
            highlight = kwargs.pop("highlight", self.settings["AUTO_HIGHLIGHT_VARS"])

            l_kwargs = {
                "settings": self._settings, 
                "highlight": highlight, 
                **kwargs.pop("extra", {})
            }
            # stackLevel is set to 3 due to external log() wrappers.
            super().log(level, msg, *args, extra=l_kwargs, stacklevel=3, **kwargs) # TODO
        else:
            self.duplicate_count += 1

    def is_duplicate(self, record_data: RecordData) -> bool:
        """ 
        Return True if the record_data is a duplicate of the previous log record data, False otherwise. 
        
        record_data -- The RecordData object that is compared to the last log record data.
        """
        return self.last_log_record_data == record_data
    
    def _log_suppress_count(self) -> bool:
        """ Return True if previous suppress count should be logged, False otherwise. """
        reached_log_threshold = self.duplicate_count >= self.settings["LOG_SUPPRESS_COUNT_THRESHOLD"]
        return reached_log_threshold

    # ~-- Wrappers --~

    def debug(self, msg, *args, **kwargs):
        self.log(logging.DEBUG, msg, *args, **kwargs)
    
    def info(self, msg, *args, **kwargs):
        """ Wrapper for calling custom info logs. """
        self.log(logging.INFO, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """ Wrapper for calling custom warning logs. """
        self.log(logging.WARNING, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """ Wrapper for calling custom error logs. """
        self.log(logging.ERROR, msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        """ Wrapper for calling custom critical logs. """
        self.log(logging.CRITICAL, msg, *args, **kwargs)

