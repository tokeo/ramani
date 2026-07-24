# Copyright 2012-2026 Tom (Thomas) Freudenberg <th.freudenberg@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0

"""
Ramani contains project blueprints for the tokeo framework.

Ramani is Kiswahili for map or blueprint. This package ships the templates
the Tokeo CLI uses to scaffold new projects. It contains no runtime logic
and imports nothing at runtime; it is a pure template payload.

The package installs into the ``tokeo`` namespace, so it sits alongside
the framework itself while shipping as its own distribution.

### Notes:

- ``tokeo`` is a PEP 420 native namespace package and carries no
    ``__init__.py``. This distribution must never ship one either, or it
    would shadow the framework's own namespace.
- The generated output belongs to the project it was generated into and
    is not subject to this package's license. Files carrying their own
    license header, currently only ``generate/project/*/core/akili/``,
    are the exception.

"""

try:
    from cement.utils.version import get_version as cement_get_version
except ModuleNotFoundError:
    # simple fallback when installing
    # version: Tuple[int, int, int, str, int])
    def cement_get_version(version):
        if version[3] == 'final':
            return f'{version[0]}.{version[1]}.{version[2]}'
        if version[3] == 'dev':
            return f'{version[0]}.{version[1]}.{version[2]}.dev.{version[4]}'
        mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'c'}
        return f'{version[0]}.{version[1]}.{version[2]}{mapping[version[3]]}{version[4]}'


VERSION = (1, 3, 0, 'final', 0)


def get_version(version=VERSION):
    return cement_get_version(version)
