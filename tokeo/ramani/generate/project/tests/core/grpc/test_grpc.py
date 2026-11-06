"""
Tests for the grpc service of {{ app_name }}: a real server as a process of
its own, reached by the grpccall client of the app.

The probe ```grpc_tests_serve_probe.py``` serves on a free port; the test
waits until ```grpccall ping``` gets its pong, then ends the server by
SIGTERM and checks that it stops cleanly.
"""

import signal

from {{ app_label }}.core.exc import {{ app_class_name }}Error
from {{ app_label }}.main import {{ app_class_name }}Test
from tests.utils import free_port
from tests.utils.process import SubProcess

#: The probe that serves grpc in a process of its own
PROBE = 'tests.core.grpc.grpc_tests_serve_probe'


def _has_pong(url):
    """True when grpccall ping gets its pong from the server at url."""
    logged = []
    argv = ['grpccall', 'ping'{% if feature_grpc_auto_certificates == "Y" %}, '--insecure'{% endif %}]
    with {{ app_class_name }}Test(argv=argv) as app:
        app.config.set('grpc', 'url', url)
        app.log.info = lambda msg, **kwargs: logged.append(msg)
        try:
            app.run()
        except {{ app_class_name }}Error:
            # not served yet, grpccall names why
            return False
    return '  response: pong' in logged


def test_grpc_serve_answers_ping_and_ends_on_term():
    """The served app answers grpccall ping and ends by SIGTERM with 0."""
    url = f'localhost:{free_port()}'
    env = {'{{ app_label | upper }}_GRPC_URL': url}
    with SubProcess.probe(PROBE, env=env) as process:
        process.wait_for(lambda: _has_pong(url))
        process.signal(signal.SIGTERM)
        assert process.wait() == 0
