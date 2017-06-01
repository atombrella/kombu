"""`nsq`_ transport.

.. _`nsq`: https://pypi.python.org/pypi/pynsq/
"""
from __future__ import absolute_import, unicode_literals

from kombu.log import get_logger
from kombu.transport import base, virtual

try:
    import nsq
except ImportError:  # pragma: no cover
    nsq = None       # noqa

DEFAULT_ADMIN_PORT_SSL = 4151
DEFAULT_PORT = 4150
DEFAULT_PORT_SSL = 443
DEFAULT_HTTP_PORT = 80
DEFAULT_HOST = 'localhost'

__all__ = ('Message', 'Channel', 'Transport'),

logger = get_logger('kombu.transport.nsq')


class Message(virtual.Message):
    """NSQ message adapted to the AMQP protocol."""

    def __init__(self, payload, channel=None, **kwargs):
        super().__init__(payload, channel, **kwargs)

    def ack(self, multiple=False):
        nsq.ready
        super().ack(multiple)

    def decode(self):
        return super().decode()

    def __repr__(self):
        return super().__repr__()


class Channel(virtual.Channel):
    """Channel for a topic in NSQ."""

    prefix = 'nsq'
    Message = nsq.Message

    def __init__(self, connection, **kwargs):
        super().__init__(connection, **kwargs)

    def Producer(self, *args, **kwargs):
        # this should be nsq.Writer which produces the
        nsq.Writer()
        return super().Producer(*args, **kwargs)

    def prepare_message(self, body, priority=None, content_type=None, content_encoding=None, headers=None,
                        properties=None):
        return body, properties

    def queue_delete(self, queue, if_unused=False, if_empty=False, **kwargs):
        super().queue_delete(queue, if_unused, if_empty, **kwargs)

    def drain_events(self, timeout=None, callback=None):
        pass

    def basic_cancel(self, consumer_tag):
        super().basic_cancel(consumer_tag)

    def Consumer(self, *args, **kwargs):
        # this should be nsq.Reader
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

    implements = base.Transport.implements.extend(
        async=True,
    )

    # connection errors and more
    connection_errors = (
        virtual.Transport.connection_errors + (
            nsq.Writer.mro(),
        )
    )

    def __init__(self, *args, **kwargs):
        if nsq is None:
            raise ImportError('Missing pynsq library')

    def establish_connection(self):
        return super().establish_connection()

    def verify_connection(self, connection):
        port = connection.client.port or self.default_port
        host = connection.client.hostname or DEFAULT_HOST

        logger.debug('Verify NSQ connection to %s:%s', host, port)

        try:
            client = nsq.AsyncConn(host=host, port=int(port))
            client.agent.self()
            return True
        except ValueError:
            pass

        return False

    def manager(self):
        return super().manager()

    def driver_version(self):
        return nsq.__version__

