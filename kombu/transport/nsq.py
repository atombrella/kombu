"""`nsq`_ transport.

.. _`nsq`: http://pypi.python.org/pynsq/
"""
from __future__ import absolute_import, unicode_literals

try:
    import nsq
except ImportError:
    nsq = None

from kombu.transport import virtual

DEFAULT_PORT = 80
DEFAULT_ADMIN_PORT = 4150
DEFAULT_ADMIN_PORT_SSL = 4151


class Message(nsq.Message, virtual.Message):
    def ack(self, multiple=False):
        super().ack(multiple)


class Channel(virtual.Channel):

    Message = Message

    def basic_qos(self, prefetch_size=0, prefetch_count=0, apply_global=False):
        super().basic_qos(prefetch_size, prefetch_count, apply_global)


class Transport(virtual.Transport):

    # list of topics
    queues = {}

    def __init__(self, client, **kwargs):
        if nsq is None:
            raise
        client = nsq.Reader()

    def get_heartbeat_interval(self, connection):
        return super().get_heartbeat_interval(connection)

    def establish_connection(self):
        nsq.Writer(name='bullshit')

    def close_channel(self, connection):
        return super().close_channel(connection)

    def driver_version(self):
        return nsq.__version__


