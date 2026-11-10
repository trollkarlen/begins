"""Extra tests for utils edge cases not covered by the original suite."""

import unittest

from begin import utils


class TestStrToBool(unittest.TestCase):

    def test_true_values(self):
        for value in ("y", "yes", "t", "true", "on", "1", "YES", "True"):
            self.assertEqual(utils.strtobool(value), 1)

    def test_false_values(self):
        for value in ("n", "no", "f", "false", "off", "0", "NO", "False"):
            self.assertEqual(utils.strtobool(value), 0)

    def test_invalid_raises(self):
        with self.assertRaises(ValueError):
            utils.strtobool("maybe")

    def test_tobool_passthrough_bool(self):
        self.assertIs(utils.tobool(True), True)
        self.assertIs(utils.tobool(False), False)

    def test_tobool_converts(self):
        self.assertIs(utils.tobool("yes"), True)
        self.assertIs(utils.tobool("off"), False)


if __name__ == "__main__":
    unittest.main()
