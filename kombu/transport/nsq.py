"""`nsq`_ transport.

.. _`nsq`: https://pypi.python.org/pypi/pynsq/
"""
from __future__ import absolute_import, unicode_literals

import socket

from kombu.transport import virtual

try:
    import nsq
except ImportError:  # pragma: no cover
    nsq = None       # noqa

DEFAULT_ADMIN_PORT_SSL = 4151
DEFAULT_PORT = 80
DEFAULT_PORT_SSL = 443

__all__ = ('Message', 'Channel', 'Transport'),


class Message(virtual.Message):
    """NSQ message adapted to the AMQP protocol."""

    def __init__(self, payload, channel=None, **kwargs):
        super().__init__(payload, channel, **kwargs)


class Channel(virtual.Channel):
    """Channel for a topic in NSQ."""

    prefix = 'nsq'
    Message = nsq.Message

    def __init__(self, connection, **kwargs):
        super().__init__(connection, **kwargs)

    def Producer(self, *args, **kwargs):
        # this should be nsq.Writer which
        nsq.Writer()
        return super().Producer(*args, **kwargs)

    def prepare_message(self, body, priority=None, content_type=None, content_encoding=None, headers=None,
                        properties=None):
        return body, properties

    def queue_delete(self, queue, if_unused=False, if_empty=False, **kwargs):
        super().queue_delete(queue, if_unused, if_empty, **kwargs)

    def basic_cancel(self, consumer_tag):
        super().basic_cancel(consumer_tag)

    def Consumer(self, *args, **kwargs):
        return super(Channel, self).Consumer(*args, **kwargs)

    @property
    def qos(self):
        return super().qos()


class Transport(virtual.Transport):
    """NSQ transport layer."""

    Channel = Channel

    default_port = DEFAULT_PORT
    driver_type = 'nsq'
    driver_name = 'nsq'

    connection_errors = (
        virtual.Transport.connection_errors + (
            ConnectionError, socket.error
        )
    )

    def __init__(self, *args, **kwargs):
        if nsq is None:
            raise ImportError('Missing pynsq library')

    def establish_connection(self):
        return super().establish_connection()

    def manager(self):
        return super().manager()

    def driver_version(self):
        return nsq.__version__

