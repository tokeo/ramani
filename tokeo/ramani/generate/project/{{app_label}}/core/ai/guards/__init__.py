"""
The project's guard implementations: positioned steps in the agent loop that
check a tool call and may deny it.

The core guards (trace_audit, tool_policy, tool_schema_validate, regex_redact,
confirm) are used straight from the config. The word filter guard is a project
example; it is re-exported here, so it can be reached from the short package
path ```{{ app_label }}.core.ai.guards``` as well as its own module.
"""

from {{ app_label }}.core.ai.guards.words import {{ app_class_name }}AiWordFilterGuard

__all__ = [
    '{{ app_class_name }}AiWordFilterGuard',
]
