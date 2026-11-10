import unittest
from unittest import mock

import begin


class FakeEntryPoint:
    """Minimal stand-in for importlib.metadata.EntryPoint for tests."""

    def __init__(self, func):
        self.name = func.__name__
        self._func = func

    def load(self):
        return self._func


class TestSubCommand(unittest.TestCase):

    def tearDown(self):
        for collector in begin.subcommands.COLLECTORS.values():
            collector.clear()

    def test_register_default(self):
        @begin.subcommand
        def one():
            pass

        @begin.subcommand
        def two():
            pass

        self.assertEqual(list(begin.subcommands.COLLECTORS[None].commands()), [one, two])

    def test_register_custom(self):
        collector = begin.subcommands.Collector()

        @begin.subcommand(collector=collector)
        def one():
            pass

        @begin.subcommand(collector=collector)
        def two():
            pass

        self.assertEqual(list(collector.commands()), [one, two])

    def test_double_register(self):
        @begin.subcommand
        def subfunction():
            pass

        with self.assertRaises(ValueError):

            @begin.subcommand
            def subfunction():
                pass

    def test_get_registered(self):
        @begin.subcommand
        def function():
            pass

        self.assertIs(begin.subcommands.COLLECTORS[None].get("function"), function)

    @mock.patch("begin.subcommands.entry_points")
    def test_entry_points(self, iep):
        def function():
            pass

        def iter_entry_points(group, *args):
            yield FakeEntryPoint(function)

        iep.side_effect = iter_entry_points
        collector = begin.subcommands.Collector()
        collector.load_plugins("entry.point")
        self.assertEqual(list(collector.commands()), [function])

    def test_named_collector(self):
        @begin.subcommand(group="named.collector")
        def function():
            pass

        self.assertEqual(len(begin.subcommands.COLLECTORS[None]), 0)
        self.assertIn("named.collector", begin.subcommands.COLLECTORS)
        self.assertIs(function, begin.subcommands.COLLECTORS["named.collector"]["function"])

    def test_named_function(self):
        @begin.subcommand(name="subcmd")
        def function():
            pass

        self.assertIn("subcmd", begin.subcommands.COLLECTORS[None])
        self.assertNotIn("function", begin.subcommands.COLLECTORS[None])
