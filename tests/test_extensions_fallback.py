"""Tests for the cgitb-free Tracebacks fallback (Python >= 3.13)."""

import contextlib
import io
import os
import sys
import tempfile
import unittest
from unittest import mock

from begin import extensions


class FakeOptions:
    """Minimal opts object as produced by argparse."""

    def __init__(self, tracebacks=False, tbdir=None):
        self.tracebacks = tracebacks
        self.tbdir = tbdir


class TestTracebacksFallback(unittest.TestCase):
    """When cgitb is unavailable (Python >= 3.13) the Tracebacks extension
    installs a sys.excepthook that writes plain-text tracebacks to stderr
    and, when --tbdir is set, to a timestamped file."""

    def setUp(self):
        self.original_excepthook = sys.excepthook
        self.tracebacks = extensions.Tracebacks(lambda: None)

    def tearDown(self):
        sys.excepthook = self.original_excepthook

    def test_disabled_installs_nothing(self):
        with mock.patch("begin.extensions.cgitb", None):
            self.tracebacks.run(FakeOptions(tracebacks=False))
        self.assertIs(sys.excepthook, self.original_excepthook)

    def test_installs_excepthook_without_cgitb(self):
        with mock.patch("begin.extensions.cgitb", None):
            self.tracebacks.run(FakeOptions(tracebacks=True, tbdir=None))
        self.assertIsNot(sys.excepthook, self.original_excepthook)

    def test_excepthook_writes_to_stderr(self):
        stderr = io.StringIO()
        with mock.patch("begin.extensions.cgitb", None):
            self.tracebacks.run(FakeOptions(tracebacks=True, tbdir=None))
        try:
            raise ValueError("boom")
        except ValueError:
            with contextlib.redirect_stderr(stderr):
                sys.excepthook(*sys.exc_info())
        self.assertIn("ValueError: boom", stderr.getvalue())

    def test_excepthook_writes_file_to_tbdir(self):
        with tempfile.TemporaryDirectory() as tbdir:
            with mock.patch("begin.extensions.cgitb", None):
                self.tracebacks.run(FakeOptions(tracebacks=True, tbdir=tbdir))
            try:
                raise ValueError("boom")
            except ValueError:
                sys.excepthook(*sys.exc_info())
            files = os.listdir(tbdir)
            self.assertEqual(len(files), 1)
            self.assertTrue(files[0].startswith("traceback-"))
            with open(os.path.join(tbdir, files[0]), encoding="utf-8") as handle:
                content = handle.read()
            self.assertIn("ValueError: boom", content)


if __name__ == "__main__":
    unittest.main()
