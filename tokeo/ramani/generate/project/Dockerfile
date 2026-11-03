{#- slim (glibc) as soon as a feature would need headers and gcc on alpine:
    there its packages install as ready wheels, alpine stays the small default -#}
{% set slim = feature_grpc == "Y" %}
FROM python:3.13-{{ "slim" if slim else "alpine" }}
LABEL MAINTAINER="{{ creator_name }} <{{ creator_email }}>"
ENV PS1="\[\e[0;33m\]\(> {{ app_label }} <\) \[\e[1;35m\]\W\[\e[0m\] \[\e[0m\]# "
ENV {{ app_label | upper }}_ENV=production

WORKDIR /app
COPY . /app

{% if slim %}
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    tzdata \
    git \
    screen \
    && rm -rf /var/lib/apt/lists/* \
    && ln -sf /usr/share/zoneinfo/UTC /etc/localtime \
    && pip install --upgrade pip \
    && pip install --no-cache-dir .
{% else %}
RUN apk add --update --no-cache \
    tzdata \
    git \
    screen \
    && ln -s /usr/share/zoneinfo/UTC /etc/localtime \
    && pip install --upgrade pip \
    && pip install --no-cache-dir .
{% endif %}

WORKDIR /app
ENTRYPOINT ["{{ app_label }}"]
