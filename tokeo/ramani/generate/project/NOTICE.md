# {{ app_name }}

Copyright {{ app_copyright }}

This product includes software developed by
{{ creator_name }} ({{ project_url }}).

{% if project_license == "Proprietary" -%}
All rights reserved. See LICENSE.txt.
{% else -%}
Licensed under {{ project_license }}, see LICENSE.txt.
{% endif %}

## Third-party components

- tokeo, Apache-2.0, Copyright 2012-2026 Tom (Thomas) Freudenberg
  (https://github.com/tokeo/tokeo)
{% if feature_ai == "Y" -%}
- tokeo-fundi, Tokeo-Fundi Source-Available License 1.0, Copyright 2026
  Tom (Thomas) Freudenberg (https://github.com/tokeo/fundi)
{% endif -%}
{% if feature_ai == "Y" and feature_ai_akili == "Y" -%}
- akili in ```{{ app_label }}/core/akili```, Apache-2.0, Copyright 2012-2026
  Tom (Thomas) Freudenberg, license text in its LICENSE.txt
{% endif -%}
