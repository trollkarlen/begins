# begins

## Overview

Command line programs for *lazy* humans.

* Decorate a function to be your programs starting point.
* Generate command line parser based on function signature.
* Search system environment for option default values.

[![CI status](https://github.com/trollkarlen/begins/actions/workflows/ci.yml/badge.svg)](https://github.com/trollkarlen/begins/actions/workflows/ci.yml)
[![Python versions](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13%20%7C%203.14%20%7C%203.15-blue)](https://www.python.org)

## Why begins?

I write a lot of small programs in [Python](https://www.python.org).
These programs often accept a small number of simple command line
arguments. Having to write command line parsing code in each of these
small programs both breaks my train of thought and greatly increases
the volume of code I am writing.

Begins was implemented to remove the boilerplate code from these Python
programs. It's not intended to replace the rich command line processing
needed for larger applications.

## Requirements

Python 3.11 or newer. There are no third-party runtime dependencies.

## Installation

This fork of *begins* is not published to the
[Python Package Index](https://pypi.org). To install the latest
development version directly from
[Github](https://github.com/trollkarlen/begins):

```bash
pip install git+https://github.com/trollkarlen/begins.git
```

Alternatively, install a versioned release using Pip and a published
release wheel or sdist (see [Releases](#releases) below):

```bash
pip install https://github.com/trollkarlen/begins/releases/download/vX.Y.Z/begins-X.Y.Z-py3-none-any.whl
```

## Releases

Versioned releases are built by CI and published on
[Github Releases](https://github.com/trollkarlen/begins/releases) with a
[Github Actions](https://github.com/trollkarlen/begins/actions)
workflow. Each release carries a universal Python wheel (`py3-none-any`)
and an sdist: *begins* is pure Python, so the same wheel installs on
Linux, macOS and Windows with CPython 3.11 or newer.

## Setting a programs starting point

The `begin.start()` function can be used as a function call or a
decorator. If called as a function it returns `True` when called from
the `__main__` module. To do this it inspects the stack frame of the
caller, checking the `__name__` global.

This allows the following Python pattern:

```python
    >>> if __name__ == '__main__':
    ...     pass

```

To be replaced with:

```python
    >>> import begin
    >>> if begin.start():
    ...    pass

```

If used as a decorator to annotate a function the function will be
called if defined in the `__main__` module as determined by inspecting
the current stack frame. Any definitions that follow the decorated
function wont be created until after the function call is complete.

Usage of `begin.start()` as a decorator looks like:

```python
    >>> import begin
    >>> @begin.start
    ... def run():
    ...     pass

```

By deferring the execution of the function until after the remainder of
the module has loaded ensures the main function doesn't fail if
depending on something defined in later code.

## Parsing command line options

If `begin.start()` decorates a function that accepts parameters,
`begin.start()` will process the command for options to pass as those
parameters:

```python
    >>> import begin
    >>> @begin.start
    ... def run(name='Arthur', quest='Holy Grail', colour='blue', *knights):
    ...     "tis but a scratch!"

```

The decorated function above will generate the following command line
help:

```text
usage: example.py [-h] [-n NAME] [-q QUEST] [-c COLOUR]
                  [knights [knights ...]]

tis but a scratch!

positional arguments:
  knights

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  (default: Arthur)
  -q QUEST, --quest QUEST
                        (default: Holy Grail)
  -c COLOUR, --colour COLOUR
                        (default: blue)
```

In Python 3, any
[function annotations](https://peps.python.org/pep-3107/)
for a parameter become the command line option help. For example:

```python
    >>> import begin
    >>> @begin.start                                         # doctest: +SKIP
    ... def run(name: 'What, is your name?',
    ...         quest: 'What, is your quest?',
    ...         colour: 'What, is your favourite colour?'):
    ...     pass

```

Will generate command help like:

```text
usage: holygrail_py3.py [-h] -n NAME -q QUEST -c COLOUR

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  What, is your name?
  -q QUEST, --quest QUEST
                        What, is your quest?
  -c COLOUR, --colour COLOUR
                        What, is your favourite colour?
```

Command line parsing supports:

* positional arguments
* keyword arguments
* default values
* variable length arguments
* annotations

Command line parsing does not support variable length keyword arguments,
commonly written as `**kwargs`. If variable length keyword arguments
are used by the decorated function an exception will be raised.

If a parameter does not have a default, failing to pass a value on the
command line will cause running the program to print an error and exit.

For programs that have a large number of options it may be preferable to
only use long options. To suppress short options, pass `False` as the
`short_args` keyword argument to the `begin.start` decorator:

```python
    >>> import begin
    >>> @begin.start(short_args=False)
    ... def run(name='Arthur', quest='Holy Grail', colour='blue', *knights):
    ...     "tis but a scratch!"

```

This program will not accept `-n`, `-q` or `-c` as option names.

Similarly, a large number of command line options may be better
displayed in alphabetical order. This can be achieved by passing
`lexical_order` as `True`:

```python
    >>> import begin
    >>> @begin.start(lexical_order=True)
    ... def main(charlie=3, alpha=1, beta=2):
    ...     pass

```

This program will list the command line options as `alpha`, `beta`,
`charlie` instead of the order in which the function accepts them.

## Further Reading

A walk-through tutorial, the remainder of this guide and API
documentation are all part of the official *begins* documentation hosted
on [Read The Docs](https://begins.readthedocs.io).

## Issues

Any bug reports or feature requests can be made using GitHub's
[issues system](https://github.com/trollkarlen/begins/issues).
