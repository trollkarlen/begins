"Help formatters for use with argparse"

# pylint: disable=unused-argument  # mixin methods keep the parent argparse signature

import argparse


class RawDescription:
    """Help message formatter which retains any formatting in descriptions.

    Based on argparse.RawDescriptionHelpFormatter from Python standard library
    Copyright 2001-2014 Python Software Foundation; All Rights Reserved
    """

    def _fill_text(self, text, width, indent):
        return "".join([indent + line for line in text.splitlines(True)])


class RawArguments:
    """Help message formatter which retains formatting of all argument text.

    Based on argparse.RawTextHelpFormatter from Python standard library
    Copyright 2001-2014 Python Software Foundation; All Rights Reserved
    """

    def _split_lines(self, text, width):
        return text.splitlines()


class ArgumentDefaults:
    """Help message formatter which adds default values to argument help.

    Based on argparse.ArgumentDefaultsHelpFormatter from Python standard library
    Copyright 2001-2014 Python Software Foundation; All Rights Reserved
    """

    def _get_help_string(self, action):
        helptext = action.help
        if "%(default)" not in action.help and action.default is not argparse.SUPPRESS:
            defaulting_nargs = [argparse.OPTIONAL, argparse.ZERO_OR_MORE]
            if action.option_strings or action.nargs in defaulting_nargs:
                helptext += " (default: %(default)s)"
        return helptext


class RemoveSubcommandsLine:
    """Removes line of subcommand names from help output.

    Based on Jeppe Ledet-Pederson's solution for hiding metavar in command
    listing. http://stackoverflow.com/a/13429281
    """

    def _format_action(self, action):
        # mixin pattern: extend argparse internals
        parts = argparse.HelpFormatter._format_action(self, action)
        if action.nargs == argparse.PARSER:
            parts = "\n".join(parts.split("\n")[1:])
        return parts


def compose(*mixins, **kwargs):
    """Compose a new help formatter class for argparse.

    Accepts a variable number of mixin class and uses these as base classes
    with multiple inheritance against argparse.HelpFormatter to create a new
    help formatter class.
    """
    if not {"name"}.issuperset(kwargs):
        unknown = set(kwargs)
        unknown.discard("name")
        msg = f"compose() got an unexpected keyword argument '{unknown.pop()}'"
        raise TypeError(msg)
    name = kwargs.get("name", "CompositeHelpFormatter")
    return type(name, tuple(mixins) + (argparse.HelpFormatter,), {})
