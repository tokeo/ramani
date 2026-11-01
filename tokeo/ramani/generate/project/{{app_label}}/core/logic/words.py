"""
Count the words of a web page, the example logic of {{ app_name }}.

The tasks of the app call it: the dramatiq actor in a worker, or the
agent, the automation, the grpc servicer and the smtpd handler directly
when the app runs without dramatiq.
"""

import requests
from tokeo.ext.appshare import app


def count_words(url):
    """
    Count the words on a web page and log the count.

    ### Args

    - **url** (str): URL of the webpage to analyze

    ### Notes

    : A page that cannot be read is logged as error, the call does not raise

    """
    try:
        response = requests.get(url, timeout=30)
        count = len(response.text.split(' '))
        app.log.info(f'There are {count} words at {url!r}.')
    except Exception as err:
        app.log.error(f'Could not count words: {err}')
