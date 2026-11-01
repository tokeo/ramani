"""
Tests for the {{ app_name }} app itself: it starts with all its extensions,
takes --debug and reads a secret of the config by the vault.
"""

from tokeo.core.vaults import VaultRef
from {{ app_label }}.main import {{ app_class_name }}Test


def test_{{ app_label }}():
    """The app runs without a command, with all extensions of its features."""
    with {{ app_class_name }}Test() as app:
        app.run()
        assert app.exit_code == 0


def test_{{ app_label }}_debug():
    """--debug switches the debug mode on."""
    with {{ app_class_name }}Test(argv=['--debug']) as app:
        app.run()
        assert app.debug is True


def test_{{ app_label }}_vault_plain_value_reads_plain_and_hides_in_repr():
    """A !vault:plain value of the config reads as text, a repr shows ***."""
    with {{ app_class_name }}Test() as app:
        app.config.merge({'example': {'password': VaultRef('plain', 's3cret')}})
        password = app.config.get('example', 'password')
        assert password == 's3cret'
        assert repr(password) == "'***'"
