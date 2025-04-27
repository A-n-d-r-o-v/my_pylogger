from colorama import init as _colorama_init, Fore, Style
import re

#from logger import _DEFAULT_SETTINGS # TODO!
import logging
from config import DEFAULT_SETTINGS

_colorama_init(autoreset=True)

# ---------------------------------

class CustomFormatter(logging.Formatter):
    """ 
    Custom formatter.
    """
    def __init__(self, str_format, *args, **kwargs):
        super().__init__(str_format, *args, **kwargs)
        self._format = str_format

    def format(self, record):
        """ 
        Custom format.
        Log only the message (without formatting) if the 'simple_formatting' flag is set to True,
        e.g: extra={'simple_formatting': True})  
        """
        settings = getattr(record, "settings", DEFAULT_SETTINGS)

        temp_fmt = self._format
        if settings["LOG_DEBUG_FORMAT_EXTRAS"]:
            temp_fmt = self._with_debug_format_extras(temp_fmt, settings["DEBUG_FORMAT_EXTRAS"])

        temp_formatter = logging.Formatter(temp_fmt, style='%')

        if getattr(record, "simple_formatting", False):
            return f"({record.levelname[0]} @ {record.name}): {record.getMessage()}"
        
        return temp_formatter.format(record)

    def _with_debug_format_extras(self, s, specifiers):
        """ 
        Apply debug specifiers to the format string 's' and return the resulting string. 
        
        s -- The format string.
        """
        specifiers = specifiers.copy()
        # Remove specifiers that already exist in the format string.
        for specifier in specifiers:
            if specifier in s:
                specifiers.remove(specifier)

        if not specifiers:
            return s
        
        # [A / B / C]
        debug_info = ' - [' + ' / '.join(specifiers) + ']'
        s += debug_info
        return s
    

# ---------------------------------


def _color_vars(s, var_color=Fore.LIGHTCYAN_EX):
    # We only have a keyword var if there is an = symbol 
    if "=" not in s:
        return s
    
    # Fat regex pattern to catch the pattern for:
    # text=variable where variable is:
    # - some text followed by a non-word character (like comma, space, dot, etc)
    # - enclosed in either [...] , (...) , {...} to colorize lists, tuples, dicts.
    # - enclosed in either "..." or '...' to colorize strings
    # Examples:
    # - "Some text lala var=42 and var2="a_string" etc etc" will catch var=42 and var2="a_string"
    # - "More text, maybe with a list i.e mylist=[a, b, c], that could be cool" will catch mylist=[a, b, c] 
    pattern = re.compile(r'(\b\w+=\s*(?:(?:"[^"]*")|(?:\'[^\']*\')|(?:\[[^\[\]]*\])|(?:\([^\(\)]*\))|(?:\{[^{}]*\})|(?:\S+)))')

    def replacer(match: re.Match) -> str:
        # The text inside the braces, including braces
        original = match.group(1)
        # Wrap found regex matches in the color
        return f"{var_color}{original}{Style.RESET_ALL}"

    return pattern.sub(replacer, s)

class ColorFormatter(CustomFormatter):
    """Color wrapper over the CustomFormatter to handle color."""
    LEVEL_COLORS = {
        logging.DEBUG:    Fore.CYAN,
        logging.INFO:     Fore.WHITE,
        logging.WARNING:  Fore.LIGHTYELLOW_EX,
        logging.ERROR:    Fore.LIGHTRED_EX,
        logging.CRITICAL: Fore.RED
    }

    def __init__(self, str_format, *args, **kwargs):
        super().__init__(str_format, *args, **kwargs)

    def format(self, record):
        msg = super().format(record)  # call CustomFormatter.format()
        
        if getattr(record, "highlight", True):    
            msg = _color_vars(msg)

        color = self.LEVEL_COLORS.get(record.levelno, "")
        return f"{color}{msg}{Style.RESET_ALL}"
    