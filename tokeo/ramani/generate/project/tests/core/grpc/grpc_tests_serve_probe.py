"""
Runs the grpc server of a {{ app_name }} test app, for the process test.

Started as its own process by test_grpc.py: the test reaches the server only
from outside, by grpccall, as a client of a real deployment does. Inside, a
regular ```{{ app_class_name }}Test``` app serves grpc until a signal ends
it; the url comes by the environment override of ```grpc.url```.
"""

from {{ app_label }}.main import {{ app_class_name }}Test


class GrpcServeProbeTest({{ app_class_name }}Test):
    """The test app of the probe, serving grpc until a signal ends it."""


def main():
    with GrpcServeProbeTest(argv=['grpc', 'serve']) as app:
        app.run()


if __name__ == '__main__':
    main()
