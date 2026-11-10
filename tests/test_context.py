import unittest
import warnings

from begin import context


class TestContext(unittest.TestCase):

    def setUp(self):
        context.clear()

    def test_swizzle(self):
        mutable = context.__class__
        with context:
            self.assertNotIsInstance(context, mutable)
        self.assertIsInstance(context, mutable)

    def test_initial_last_return(self):
        self.assertIsNone(context.last_return)

    def test_deprecation_warning(self):
        with warnings.catch_warnings(record=True) as warned:
            warnings.simplefilter("always")
            _ = context.return_value
        self.assertGreater(len(warned), 0)

    def test_mutable(self):
        for name in context._protected:
            if name.startswith("_"):
                continue
            setattr(context, name, None)

    def test_immutable(self):
        with context:
            for name in context._protected:
                if name.startswith("_"):
                    continue
                self.assertRaises(AttributeError, setattr, context, name, None)

    def test_protected(self):
        self.assertRaises(AttributeError, setattr, context, "alpha", None)
