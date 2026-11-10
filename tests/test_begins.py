import doctest
import os
import sys
import unittest

import begin


class TestBegins(unittest.TestCase):

    def test_has_version(self):
        self.assertTrue(begin.__version__)

    def test_readme(self):
        # doctest.testfile never raises on failing examples - assert on the
        # result so README regressions actually fail the suite.
        readme = os.path.join(os.path.dirname(__file__), "..", "README.md")
        try:
            original = sys.argv
            sys.argv = [""]
            result = doctest.testfile(readme, module_relative=False)
        finally:
            sys.argv = original
            for collector in begin.subcommands.COLLECTORS.values():
                collector.clear()
        # The README contains 13 examples, one guarded with
        # "# doctest: +SKIP". Python counts a skipped example in
        # TestResults.attempted from 3.13 onwards but not on 3.11/3.12,
        # so pin the count down to the non-skipped examples and forbid
        # any failing example.
        self.assertGreaterEqual(result.attempted, 12)
        self.assertEqual(result.failed, 0)


if __name__ == "__main__":
    unittest.main()
