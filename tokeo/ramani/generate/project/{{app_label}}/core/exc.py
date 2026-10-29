class {{ app_class_name }}BaseException(BaseException):
    """
    Base of all exceptions of {{ app_class_name }}.

    ### Notes

    : {{ app_class_name }}Error derives from Exception and from this class, so
        it stays an Exception; an exception that only derives from this class
        passes ```except Exception```

    : The exceptions of {{ app_class_name }} are independent of those of tokeo

    """

    pass


class {{ app_class_name }}Error(Exception, {{ app_class_name }}BaseException):
    """Generic {{ app_class_name }} errors."""

    pass
