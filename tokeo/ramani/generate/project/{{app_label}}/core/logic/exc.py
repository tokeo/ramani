from {{ app_label }}.core.exc import {{ app_class_name }}Error


class {{ app_class_name }}LogicError({{ app_class_name }}Error):
    """The {{ app_name }} logic errors."""

    pass
