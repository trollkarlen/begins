"""Utility functions for begins"""

from argparse import FileType as tofile

_TRUE = {"y", "yes", "t", "true", "on", "1"}
_FALSE = {"n", "no", "f", "false", "off", "0"}

__all__ = ["tofile", "tolist", "tobool", "strtobool"]


def strtobool(value):
    """Convert a string representation of truth to 1 or 0.

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'value' is anything else.

    Replaces distutils.util.strtobool, which was removed together with
    distutils in Python 3.12.
    """
    val = str(value).lower()
    if val in _TRUE:
        return 1
    if val in _FALSE:
        return 0
    raise ValueError(f"invalid truth value {value!r}")


def tobool(value):
    """Convert a string representation of truth to True or False.

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'value' is anything else.
    """
    if isinstance(value, bool):
        return value
    return bool(strtobool(value))


def tolist(value=None, sep=",", empty_strings=False):
    """Convert a separated string to a list of strings.

    Called with a value, splits the string on 'sep' and returns the
    stripped items. Empty items are dropped unless 'empty_strings' is
    true.  Called without a value, returns a converter function with the
    given options bound, suitable for use with begin.convert().
    """

    def convert(value_):
        items = [item.strip() for item in str(value_).split(sep)]
        if not empty_strings:
            items = [item for item in items if item != ""]
        return items

    if value is None:
        return convert
    return convert(value)
