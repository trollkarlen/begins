"Subcommand support for command lines"

from collections import defaultdict
from collections.abc import MutableMapping
from importlib.metadata import entry_points


class Collector(dict):
    """Collect functions for use as subcommands"""

    def commands(self):
        "Yield the registered subcommand functions in name order"
        for name in sorted(self):
            yield self[name]

    def load_plugins(self, entry_point):
        "Load subcommand functions registered at the given entry point"
        for entry in entry_points(group=entry_point):
            self.register(entry.load(), name=entry.name)

    def register(self, func, name=None):
        "Register a subcommand function, optionally under another name"
        name = func.__name__ if name is None else name
        if name in self:
            msg = f"Function named '{name}' already registered"
            raise ValueError(msg)
        self[name] = func


def subcommand(func=None, name=None, group=None, collector=None):
    """Register function as a program's subcommand

    Functions are registered with the default subcommand collector, unless a
    custom collector is provided through the 'collector' argument. Subcommands
    will automatically be included in the generated command line support.
    """

    def wrapper(func):
        collector.register(func, name=name)
        return func

    collector = COLLECTORS[group] if collector is None else collector
    if func is not None:
        return wrapper(func)
    return wrapper


COLLECTORS: MutableMapping[str | None, Collector] = defaultdict(Collector)
