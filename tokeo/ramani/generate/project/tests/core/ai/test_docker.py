"""
Test cases for the docker sandbox of the {{ app_name }} ai setup.

A fake ```docker``` command first on the PATH stands in for the client: it logs
its arguments and starts the generic runner locally, so the agent
```contained``` runs ```calc``` through the real config without a docker service.
The live test runs only when docker reaches the image ```{{ app_label }}:latest```
(```make docker```).
"""

import os
import sys
import json
import shutil
import subprocess

import pytest
from {{ app_label }}.main import {{ app_class_name }}Test

#: A fake docker command: it logs its arguments and runs the python command of
#: the container on the host
DOCKER_FAKE_SCRIPT = """#!{python}
import os, sys, json
args = sys.argv[1:]
with open({log!r}, 'a') as log:
    log.write(json.dumps(args) + '\\n')
python = args.index('-m') - 1
os.chdir({root!r})
os.execve(sys.executable, [sys.executable] + args[python + 1 :], dict(PYTHONPATH={root!r}))
"""


class {{ app_class_name }}DockerTestApp({{ app_class_name }}Test):

    class Meta:
        # set framework extensions
        extensions = [
            'colorlog',
            'tokeo.ext.yaml',
            'tokeo.ext.vault',
            'tokeo.ext.appenv',
            'tokeo.ext.print',
            'tokeo.ext.jinja2',
            'tokeo.ext.appshare',
            'tokeo.ext.ai',
        ]


def image_ready():
    # docker is installed and the image of the app is built
    if not shutil.which('docker'):
        return False
    try:
        probe = subprocess.run(['docker', 'image', 'inspect', '{{ app_label }}:latest'], capture_output=True, timeout=20)
    except (OSError, subprocess.TimeoutExpired):
        return False
    return probe.returncode == 0


def test_{{ app_label }}_ai_docker_sandbox_runs_calc_hardened(tmp_path, monkeypatch):
    # the agent contained runs calc in the sandbox docked: one throwaway
    # container of the app's image, every hardening flag, python as entrypoint
    log = tmp_path / 'calls.log'
    fake = tmp_path / 'docker'
    fake.write_text(DOCKER_FAKE_SCRIPT.format(python=sys.executable, log=str(log), root=os.getcwd()))
    fake.chmod(0o755)
    monkeypatch.setenv('PATH', f'{tmp_path}{os.pathsep}{os.environ["PATH"]}')
    with {{ app_class_name }}DockerTestApp() as app:
        result = app.ai.chat([{'role': 'user', 'content': 'calc 2 + 3'}], agent='contained', profile='mock')
    assert result.answer.text == 'Done. The tool returned: 5'
    [args] = [json.loads(line) for line in log.read_text().splitlines()]
    assert args[:3] == ['run', '--rm', '-i']
    for flag, value in (('--cap-drop', 'ALL'), ('--security-opt', 'no-new-privileges'), ('--network', 'none'), ('--memory', '256m')):
        assert args[args.index(flag) + 1] == value
    assert '--read-only' in args and '--privileged' not in args
    start = args.index('--entrypoint')
    assert args[start:] == ['--entrypoint', 'python3', '{{ app_label }}:latest', '-m', 'tokeo.core.ai.sandboxes.runner']


@pytest.mark.skipif(not image_ready(), reason='needs docker and the image {{ app_label }}:latest (make docker)')
def test_{{ app_label }}_ai_docker_sandbox_live():
    # with a real docker the calc tool answers from a container
    with {{ app_class_name }}DockerTestApp() as app:
        result = app.ai.chat([{'role': 'user', 'content': 'calc 2 + 3'}], agent='contained', profile='mock')
    assert result.answer.text == 'Done. The tool returned: 5'
