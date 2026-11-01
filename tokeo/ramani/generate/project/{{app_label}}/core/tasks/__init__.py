"""
The {{ app_name }} task collection: actors, automations, agents,
operators, performers, and steps; lazily loaded so importing the
package stays cheap until a task module is touched.
"""

import lazy_loader as lazy

__getattr__, __dir__, __all__ = lazy.attach(
    __name__,
    submodules=[
{% if feature_dramatiq == "Y" %}
        'actors',
{% endif %}
{% if feature_automate == "Y" %}
        'automate',
{% endif %}
{% if feature_apscheduler == "Y" %}
        'agents',
{% endif %}
        'operators',
        'performers',
        'steps',
    ],
)
