# cement is a build requirement, the build and the app count the version alike
from cement.utils.version import get_version as cement_get_version

#: The version of the app as (major, minor, patch, release, number)
VERSION = (0, 0, 1, 'alpha', 0)


def get_version(version=VERSION):
    return cement_get_version(version)
