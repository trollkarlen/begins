"Command line extension plugins"
import cgitb
import logging
import logging.handlers
import platform
import sys

from begin.wrappable import Wrapping
from begin.utils import tobool

__all__ = ['logger', 'tracebacks']


class Extension(Wrapping):
    """Base class of all command line extensions

    Extension are required to subclass this class and override the
    add_arguments() and run() methods.
    """

    def add_arguments(self, parser, defaults):
        "Add command line arguments to parser"
        raise NotImplementedError("Command line extension incomplete")

    def run(self, opts):
        "run extension using command line options"
        raise NotImplementedError("Command line extension incomplete")


class Tracebacks(Extension):
    "Manage command line extension for cgitb module"

    section = 'tracebacks'

    def add_arguments(self, parser, defaults):
        "Add command line arguments for configuring traceback module"
        group = parser.add_argument_group('tracebacks',
                'Extended traceback reports on failure')
        group.add_argument('--tracebacks', action='store_true',
                default=tobool(defaults.from_name(
                    'enable', section=self.section, default='false')),
                help='Enable extended traceback reports')
        group.add_argument('--tbdir',
                default=defaults.from_name(
                    'directory', section=self.section, default=None),
                help='Write tracebacks to directory')

    def run(self, opts):
        "Configure cgitb module if enabled on command line"
        if not opts.tracebacks:
            return
        cgitb.enable(logdir=opts.tbdir, format='txt')


def tracebacks(func):
    "Add command line extension for cgitb module"
    return Tracebacks(func)


class Logging(Extension):
    "Manage command line extension for the logging module"

    section = 'logging'

    def __init__(self, func, stream_file=sys.stderr, name=None, logfmt=None, stream_logfmt=None, file_logfmt=None, **kwargs):
        Extension.__init__(self, func)
        self._stream_file = stream_file
        self._logger_name = name
        self._stream_logfmt = stream_logfmt if stream_logfmt else logfmt
        self._file_logfmt = file_logfmt if file_logfmt else logfmt

    def add_arguments(self, parser, defaults):
        "Add command line arguments for configuring the logging module"
        exclusive  = parser.add_mutually_exclusive_group()
        exclusive.add_argument('-v', '--verbose',
                default=False, action='store_true',
                help='Increse logging output')
        exclusive.add_argument('-q', '--quiet',
                default=False, action='store_true',
                help='Decrease logging output')
        group = parser.add_argument_group('logging',
                'Detailed control of logging output')
        group.add_argument('--loglvl',
                default=defaults.from_name(
                    'level', section=self.section, default=None),
                choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                help='Set explicit log level')
        group.add_argument('--logfile',
                default=defaults.from_name(
                    'file', section=self.section, default=None),
                help='Output log messages to file')
        group.add_argument('--logfmt',
                default=defaults.from_name(
                    'format', section=self.section, default=None),
                help='Log message format')

    def run(self, opts):
        "Configure logging module according to command line options"
        # log level
        level = logging.INFO
        if opts.loglvl is not None:
            level = logging.getLevelName(opts.loglvl)
        elif opts.verbose:
            level = logging.DEBUG
        elif opts.quiet:
            level = logging.WARNING
        # logger
        logger = logging.getLogger(self._logger_name)
        for handler in logger.handlers:
            logger.removeHandler(handler)
        logger.setLevel(level)
        # handler
        if opts.logfile is None:
            handler = logging.StreamHandler(self._stream_file)
        elif platform.system() != 'Windows':
            handler = logging.handlers.WatchedFileHandler(opts.logfile)
        else:
            handler = logging.FileHandler(opts.logfile)
        logger.addHandler(handler)
        # formatter
        fmt = opts.logfmt
        if fmt is None:
            if opts.logfile is None:
                if self._stream_logfmt:
                    fmt = self._stream_logfmt
                else:
                    fmt = '%(message)s'
            else:
                if self._file_logfmt:
                    fmt = self._file_logfmt
                else:
                    fmt = '[%(asctime)s] [%(levelname)s] [%(pathname)s:%(lineno)s] %(message)s'
        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)


def logger(func=None, **kwargs):
    "Add command line extension for logging module"
    def _start(func):
        prog = Logging(func, **kwargs)
        return prog

    # logger() is a decorator factory
    if func is None and len(kwargs) > 0:
        return _start

    return Logging(func)
