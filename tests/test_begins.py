import doctest
import os
import sys
import unittest

import begin


class TestBegins(unittest.TestCase):

    def test_has_version(self):
        self.assertTrue(begin.__version__)

    def test_readme(self):
        readme = os.path.join(os.path.dirname(__file__), "..", "README.rst")
        try:
            original = sys.argv
            sys.argv = [""]
            doctest.testfile(readme, module_relative=False)
        finally:
            sys.argv = original
            for collector in begin.subcommands.COLLECTORS.values():
                collector.clear()


if __name__ == "__main__":
    unittest.main()
