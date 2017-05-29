"""`nsq`_ transport.

.. _`nsq`: https://pypi.python.org/pypi/pynsq/
"""
from __future__ import absolute_import, unicode_literals

from kombu.transport import base, virtual
from kombu.messaging import Exchange

try:
    import nsq
except ImportError:  # pragma: no cover
    nsq = None       # noqa

DEFAULT_ADMIN_PORT_SSL = 4151
DEFAULT_PORT = 80
DEFAULT_PORT_SSL = 443


class Message(nsq.Message, base.Message):

    def __init__(self, id, body, timestamp, attempts):
        super(self, base.Message).__init__(body=body)

    def requeue(self):
        return super().requeue()

    def enable_async(self):
        super().enable_async()

    def finish(self):
        super().finish()


class Channel(virtual.Channel):
    prefix = 'nsq'
    Message = Message

    def prepare_message(self, body, priority=None, content_type=None, content_encoding=None, headers=None,
                        properties=None):
        return super().prepare_message(body, priority, content_type, content_encoding, headers, properties)

    def queue_delete(self, queue, if_unused=False, if_empty=False, **kwargs):
        super().queue_delete(queue, if_unused, if_empty, **kwargs)

    def Consumer(self, *args, **kwargs):
        return super(Channel, self).Consumer(*args, **kwargs)

    def __init__(self):
        nsq.AsyncConn()

    @property
    def qos(self):
        return super().qos()


class Transport(virtual.Transport):
    Channel = Channel

    default_port = DEFAULT_PORT
    driver_type = 'nsq'
    driver_name = 'nsq'

    def __init__(self, *args, **kwargs):
        if nsq is None:
            raise ImportError('Missing pynsq library')

    def driver_version(self):
        return nsq.__version__

    def close_channel(self, channel):
        nsq.AsyncConn.
        super().close_channel(channel)
