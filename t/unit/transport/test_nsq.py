from __future__ import absolute_import, unicode_literals

from case import Mock, skip

from funtests import transport


@skip.unless_module('nsq')
class NSQTest(transport.TransportCase):
    transport = 'pynsq'
    prefix = 'pynsq'
