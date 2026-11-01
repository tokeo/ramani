# Copyright 2012-2026 Tom (Thomas) Freudenberg <th.freudenberg@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0

"""
Ramani contains project blueprints for the tokeo framework.

Ramani is Kiswahili for map or blueprint. This package ships the templates
the Tokeo CLI uses to scaffold new projects. It contains no runtime logic
and imports only cement for its version; it is a pure template payload.

The package installs into the ```tokeo``` namespace, so it sits alongside
the framework itself while shipping as its own distribution.

### Notes

- ```tokeo``` is a PEP 420 native namespace package and carries no
    ```__init__.py```. This distribution must never ship one either, or it
    would shadow the framework's own namespace.
- The generated output belongs to the project it was generated into and
    is not subject to this package's license. Files carrying their own
    license header, currently only ```generate/project/*/core/akili/```,
    are the exception.

"""

# the templates are no modules of their own, pdoc skips the generate folder
__pdoc__ = {
    'generate': False,
}

# cement is a build requirement, the build and the app count the version alike
from cement.utils.version import get_version as cement_get_version

VERSION = (2, 2, 0, 'final', 0)


def get_version(version=VERSION):
    return cement_get_version(version)
