# coding: utf-8

# Python libs
from __future__ import absolute_import
import logging

# Salt testing libs
from tests.support.unit import skipIf, TestCase
from tests.support.mock import NO_MOCK, NO_MOCK_REASON, patch, MagicMock, mock_open
from tests.support.mixins import LoaderModuleMockMixin

# Salt libs
import salt.beacons.btmp as btmp
from salt.ext import six

raw = b'\x06\x00\x00\x00Nt\x00\x00ssh:notty\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00garet\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00::1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xdd\xc7\xc2Y\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
pack = (6, 29774, b'ssh:notty\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', b'\x00\x00\x00\x00', b'garet\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', b'::1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', 0, 0, 0, 1505937373, 0, 0, 0, 0, 16777216)

log = logging.getLogger(__name__)


@skipIf(NO_MOCK, NO_MOCK_REASON)
class BTMPBeaconTestCase(TestCase, LoaderModuleMockMixin):
    '''
    Test case for salt.beacons.[s]
    '''

    def setup_loader_modules(self):
        return {
            btmp: {
                '__context__': {'btmp.loc': 2},
                '__salt__': {},
            }
        }

    def test_non_list_config(self):
        config = {}
        ret = btmp.validate(config)

        self.assertEqual(ret, (False, 'Configuration for btmp beacon must'
                                      ' be a list.'))

    def test_empty_config(self):
        config = [{}]

        ret = btmp.validate(config)

        self.assertEqual(ret, (True, 'Valid beacon configuration'))

    def test_no_match(self):
        config = [{'users': {'gareth': {'time': {'end': '5pm',
                                                 'start': '3pm'}}}}
                  ]

        ret = btmp.validate(config)

        self.assertEqual(ret, (True, 'Valid beacon configuration'))

        with patch('salt.utils.files.fopen', mock_open()) as m_open:
            ret = btmp.beacon(config)
            call_args = next(six.itervalues(m_open.filehandles))[0].call_args
            assert call_args == (btmp.BTMP, 'rb'), call_args
            assert ret == [], ret

    def test_match(self):
        with patch('salt.utils.files.fopen',
                   mock_open(read_data=raw)):
            with patch('struct.unpack',
                       MagicMock(return_value=pack)):
                config = [{'users': {'garet': {}}}]

                ret = btmp.validate(config)

                self.assertEqual(ret, (True, 'Valid beacon configuration'))

                _expected = [{'addr': 1505937373,
                              'exit_status': 0,
                              'inittab': '',
                              'hostname': '::1',
                              'PID': 29774,
                              'session': 0,
                              'user':
                              'garet',
                              'time': 0,
                              'line': 'ssh:notty',
                              'type': 6}]
                ret = btmp.beacon(config)
                self.assertEqual(ret, _expected)

    def test_match_time(self):
        with patch('salt.utils.files.fopen',
                   mock_open(read_data=raw)):
            with patch('time.time',
                       MagicMock(return_value=1506121200)):
                with patch('struct.unpack',
                           MagicMock(return_value=pack)):
                    config = [{'users': {'garet': {'time': {'end': '5pm',
                                                            'start': '3pm'}}}}
                              ]

                    ret = btmp.validate(config)

                    self.assertEqual(ret, (True, 'Valid beacon configuration'))

                    _expected = [{'addr': 1505937373,
                                  'exit_status': 0,
                                  'inittab': '',
                                  'hostname': '::1',
                                  'PID': 29774,
                                  'session': 0,
                                  'user':
                                  'garet',
                                  'time': 0,
                                  'line': 'ssh:notty',
                                  'type': 6}]
                    ret = btmp.beacon(config)
                    self.assertEqual(ret, _expected)
