"Program execution context"

import warnings


class SwizzleContext:
    """Type switching context object base class

    Supports the context manager protocol to switch the instance from a
    MutableContext to the protected Context.
    """

    _protected = {"_protected": None, "opts_current": None, "opts_next": (), "opts_previous": (), "return_values": ()}

    def __enter__(self):
        "Switch the instance to the protected Context class"
        self.__class__ = Context
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        "Switch the instance back to the mutable MutableContext class"
        self.__class__ = MutableContext

    @property
    def last_return(self):
        "The most recent return value from an applied command line"
        try:
            # "return_values" is created dynamically by clear()
            return self.return_values[-1]
        except IndexError:
            return None

    @property
    def return_value(self):
        "Deprecated alias of last_return"
        warnings.warn("The 'return_value' property will be removed in future versions.  Use 'last_return' instead.", DeprecationWarning, stacklevel=2)
        return self.last_return


class MutableContext(SwizzleContext):
    """Mutable context object

    Only protected properties may be assigned to. Constructor ensures all
    protected properties are initialised correctly.
    """

    def __init__(self):
        self.clear()

    def __setattr__(self, name, value):
        if not name.startswith("__") and name not in self._protected:
            msg = f"attempt to assign value to to immutable attribute '{name}'"
            raise AttributeError(msg)
        object.__setattr__(self, name, value)

    def clear(self):
        "Reset all unprotected properties to their initial values"
        for name, value in self._protected.items():
            if name.startswith("_"):
                continue
            setattr(self, name, value)


class Context(SwizzleContext):
    """Protected context object

    Attempts to assign to protected properties will raise an AttributeError.
    """

    def __setattr__(self, name, value):
        if name in self._protected:
            msg = f"attempt to assign value to to immutable attribute '{name}'"
            raise AttributeError(msg)
        object.__setattr__(self, name, value)


context = MutableContext()
