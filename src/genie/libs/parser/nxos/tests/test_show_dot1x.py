#!/bin/env python
# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock
from ats.topology import Device

from genie.metaparser.util.exceptions import SchemaEmptyParserError, SchemaMissingKeyError
from genie.libs.parser.nxos.show_dot1x import ShowDot1xAllStatistics, \
                                                ShowDot1xAllSummary, \
                                                    ShowDot1xAllDetails


#   ============================================    #
#                    Statistics                     #
#   ============================================    #

class test_show_dot1x_all_statistics(unittest.TestCase):
    dev1 = Device(name='DeviceA')
    dev2 = Device(name='DeviceB')

    empty_output = {'execute.return_value' : '          '}

    parsed_output = {
        'interfaces': {
            'Ethernet1/1': {
                'interface': 'Ethernet1/1',
                'statistics': {
                    'txreq': 0,
                    'rxlogoff': 0,
                    'txtotal': 3,
                    'txreqid': 0,
                    'lastrxsrcmac': '00:00:00:00:00:00',
                    'rxinvalid': 0,
                    'rxrespid': 0,
                    'rxlenerr': 0,
                    'rxversion': 0,
                    'rxstart': 0,
                    'rxresp': 0,
                    'rxtotal': 0,
                }
            }
        }
    }

    output = {'execute.return_value': '''
        Dot1x Authenticator Port Statistics for Ethernet1/1
        --------------------------------------------
        RxStart = 0     RxLogoff = 0    RxResp = 0      RxRespID = 0
        RxInvalid = 0   RxLenErr = 0    RxTotal = 0

        TxReq = 0       TxReqID = 0     TxTotal = 3

        RxVersion = 0   LastRxSrcMAC = 00:00:00:00:00:00
    '''}

    parsed_output_2 = {
        'interfaces': {
            'Ethernet1/1': {
                'interface': 'Ethernet1/1',
                'statistics': {
                    'txreq': 5,
                    'rxlogoff': 25,
                    'txtotal': 6,
                    'txreqid': 89,
                    'lastrxsrcmac': '02:45:44:55:66:78',
                    'rxinvalid': 5,
                    'rxrespid': 34,
                    'rxlenerr': 6,
                    'rxversion': 78,
                    'rxstart': 111,
                    'rxresp': 224,
                    'rxtotal': 543,
                }
            }
        }
    }

    output_2 = {'execute.return_value': '''
        Dot1x Authenticator Port Statistics for Ethernet1/1
        --------------------------------------------
        RxStart = 111     RxLogoff = 25    RxResp = 224      RxRespID = 34
        RxInvalid = 5   RxLenErr = 6    RxTotal = 543

        TxReq = 5       TxReqID = 89     TxTotal = 6

        RxVersion = 78   LastRxSrcMAC = 02:45:44:55:66:78 
    '''}

    def test_output(self):
        self.maxDiff = None
        self.dev1 = Mock(**self.output)
        obj = ShowDot1xAllStatistics(device=self.dev1)
        parsed = obj.parse()
        self.assertEqual(parsed, self.parsed_output)

    def test_output_2(self):
        self.maxDiff = None
        self.dev1 = Mock(**self.output_2)
        obj = ShowDot1xAllStatistics(device=self.dev1)
        parsed = obj.parse()
        self.assertEqual(parsed, self.parsed_output_2)

    def test_empty_output(self):
        self.dev2 = Mock(**self.empty_output)
        obj = ShowDot1xAllStatistics(device = self.dev2)
        with self.assertRaises(SchemaEmptyParserError):
            parsed = obj.parse()


#   ============================================    #
#                     Summary                       #
#   ============================================    #

class test_show_dot1x_all_summary(unittest.TestCase):
    dev1 = Device(name = 'DeviceA')
    dev2 = Device(name = 'DeviceB')

    empty_output = {'execute.return_value' : '       '}

    parsed_output_1 = {
        'interfaces': {
            'Ethernet102/1/6': {
                'interface': 'Ethernet102/1/6',
                'clients': {
                    '0E:BE:EF:3F:00:00': {
                        'client': '0E:BE:EF:3F:00:00',
                        'pae': 'AUTH',
                        'status': 'AUTHORIZED'
                    }
                }
            },
            'Ethernet1/1': {
                'interface': 'Ethernet1/1',
                'clients': {
                    'none' : {
                        'client': 'none',
                        'pae': 'AUTH',
                        'status': 'AUTHORIZED'
                    }
                }
            }
        }
    }

    output = {'execute.return_value' : '''
               Interface     PAE              Client          Status
    ------------------------------------------------------------------
             Ethernet1/1    AUTH                none      AUTHORIZED

               Interface     PAE              Client          Status
    ------------------------------------------------------------------
      Ethernet102/1/6    AUTH   0E:BE:EF:3F:00:00      AUTHORIZED
    '''}

    parsed_output_2 = {
        'interfaces': {
            'Ethernet5': {
                'interface': 'Ethernet5',
                'clients': {
                    '0e:be:00:4g:e0:00': {
                        'client': '0e:be:00:4g:e0:00',
                        'pae': 'SUPP',
                        'status': 'UNAUTHORIZED'
                    }
                }
            },
            'Ethernet1/1': {
                'interface': 'Ethernet1/1',
                'clients': {
                    'none': {
                        'client': 'none',
                        'pae': 'AUTH',
                        'status': 'AUTHORIZED'
                    }
                }
            }
        }
    }

    output_2 = {'execute.return_value' : '''
               Interface     PAE              Client          Status
    ------------------------------------------------------------------
             Ethernet1/1    AUTH                none      AUTHORIZED

               Interface     PAE              Client          Status
    ------------------------------------------------------------------
      Ethernet5    SUPP   0e:be:00:4g:e0:00      UNAUTHORIZED
    '''}

    # Tests
    def test_output_1(self):
        self.maxDiff = None
        self.dev1 = Mock(**self.output)
        obj = ShowDot1xAllSummary(device = self.dev1)
        parsed = obj.parse()
        self.assertEqual(parsed, self.parsed_output_1)

    def test_output_2(self):
        self.maxDiff = None
        self.dev1 = Mock(**self.output_2)
        obj = ShowDot1xAllSummary(device = self.dev1)
        parsed = obj.parse()
        self.assertEqual(parsed, self.parsed_output_2)
    
    def test_empty_output(self):
        self.dev2 = Mock(**self.empty_output)
        obj = ShowDot1xAllSummary(device = self.dev2)
        with self.assertRaises(SchemaEmptyParserError):
            parsed = obj.parse()


#   ============================================    #
#                     Details                       #
#   ============================================    #

class test_show_dot1x_all_details(unittest.TestCase):
    dev1 = Device(name = 'DeviceA')
    dev2 = Device(name = 'DeviceB')


    parsed_output = {
        'system_auth_control': True,
        'version': 2,
        'interfaces': {
            'Ethernet1/1': {
                'interface': 'Ethernet1/1',
                'pae': 'authenticator',
                'port_control': 'force_auth',
                'host_mode': 'single host',
                're_authentication': False,
                'timeout': {
                    'quiet_period': 60,
                    'server_timeout': 30,
                    'supp_timeout': 30,
                    'tx_period': 30,
                    'ratelimit_period': 0
                },
                're_auth_max': 2,
                'max_req': 2,
                'mac-auth-bypass': False,
                'port_status': 'authorized'
            },
            'Ethernet1/2': {
                'interface': 'Ethernet1/2',
                'pae': 'authenticator',
                'port_control': 'auto',
                'host_mode': 'single host',
                're_authentication': True,
                'timeout': {
                    'quiet_period': 60,
                    'server_timeout': 30,
                    'supp_timeout': 30,
                    'tx_period': 30,
                    'ratelimit_period': 0,
                    're_auth_period': 60,
                    'time_to_next_reauth': 17
                },
                're_auth_max': 2,
                'max_req': 3,
                'mac-auth-bypass': False,
                'clients': {
                    '54:be:ef:e5:00:00' : {
                        'client': '54:be:ef:e5:00:00',
                        'session': {
                            'auth_sm_state': 'authenticated',
                            'auth_bend_sm_state': 'idle',
                            'auth_by': 'remote server',
                            'reauth_action': 'reauthenticate'
                        },
                        'auth_method': 'eap'
                    },
                },
                'port_status': 'authorized'
            }
        }
    }

    output =  {'execute.return_value': '''
                   Sysauthcontrol Enabled   
           Dot1x Protocol Version 2         

        Dot1x Info for Ethernet1/1
        -----------------------------------
                              PAE = AUTHENTICATOR
                      PortControl = FORCE_AUTH
                         HostMode = SINGLE HOST
                 ReAuthentication = Disabled
                      QuietPeriod = 60
                    ServerTimeout = 30
                      SuppTimeout = 30
                     ReAuthPeriod = 3600 (Locally configured)
                        ReAuthMax = 2
                           MaxReq = 2
                         TxPeriod = 30
                  RateLimitPeriod = 0
                  Mac-Auth-Bypass = Disabled

        Dot1x Authenticator Client List Empty

                      Port Status = AUTHORIZED

                   Sysauthcontrol Enabled   
           Dot1x Protocol Version 2 

        Dot1x Info for Ethernet1/2
        -----------------------------------
                              PAE = AUTHENTICATOR
                      PortControl = AUTO
                         HostMode = SINGLE HOST
                 ReAuthentication = Enabled
                      QuietPeriod = 60
                    ServerTimeout = 30
                      SuppTimeout = 30
                     ReAuthPeriod = 60 (From Authentication Server)
                        ReAuthMax = 2
                           MaxReq = 3
                         TxPeriod = 30
                  RateLimitPeriod = 0
                  Mac-Auth-Bypass = Disabled

        Dot1x Authenticator Client List
        -------------------------------
                       Supplicant = 54:BE:EF:E5:00:00
                Auth SM State = AUTHENTICATED
                Auth BEND SM State = IDLE
                      Port Status = AUTHORIZED
            Authentication Method = EAP
                 Authenticated By = Remote Server
                     ReAuthPeriod = 60
                     ReAuthAction = Reauthenticate
                 TimeToNextReauth = 17
    '''}


    parsed_output_2 = {
        'system_auth_control': False,
        'version': 3,
        'interfaces': {
            'Ethernet1/2': {
                'interface': 'Ethernet1/2',
                'pae': 'authenticator',
                'port_control': 'not auto',
                'host_mode': 'double host',
                're_authentication': False,
                'timeout': {
                    'quiet_period': 59,
                    'server_timeout': 29,
                    'supp_timeout': 29,
                    'tx_period': 29,
                    'ratelimit_period': 1,
                    're_auth_period': 59,
                    'time_to_next_reauth': 16
                },
                're_auth_max': 1,
                'max_req': 2,
                'mac-auth-bypass': True,
                'clients': {
                    '53:ab:de:d4:11:11' : {
                        'client': '53:ab:de:d4:11:11',
                        'session': {
                            'auth_sm_state':'authenticated',
                            'auth_bend_sm_state': 'idle',
                            'auth_by': 'remote',
                            'reauth_action': 'reauthenticate'
                        },
                        'auth_method': 'eap'
                    },
                },
                'port_status': 'authorized'
            }
        }
    }

    output_2 = {'execute.return_value':'''
                   Sysauthcontrol Disabled
           Dot1x Protocol Version 3 

        Dot1x Info for Ethernet1/2
        -----------------------------------
                              PAE = AUTHENTICATOR
                      PortControl = NOT AUTO
                         HostMode = DOUBLE HOST
                 ReAuthentication = DISABLE
                      QuietPeriod = 59
                    ServerTimeout = 29
                      SuppTimeout = 29
                     ReAuthPeriod = 59 (From Authentication Server)
                        ReAuthMax = 1
                           MaxReq = 2
                         TxPeriod = 29
                  RateLimitPeriod = 1
                  Mac-Auth-Bypass = ENABLED

        Dot1x Authenticator Client List
        -------------------------------
                       Supplicant = 53:AB:DE:D4:11:11
                Auth SM State = AUTHENTICATED
                Auth BEND SM State = IDLE
                      Port Status = AUTHORIZED
            Authentication Method = EAP
                 Authenticated By = Remote
                     ReAuthPeriod = 59
                     ReAuthAction = reauthenticate
                 TimeToNextReauth = 16
    '''}

    empty_output = {'execute.return_value' : '          '}

    def test_output_1(self):
        self.maxDiff = None
        self.dev1 = Mock(**self.output)
        obj = ShowDot1xAllDetails(device = self.dev1)
        parsed = obj.parse()
        self.assertEqual(parsed, self.parsed_output)

    def test_output_2(self):
        self.maxDiff = None
        self.dev1 = Mock(**self.output_2)
        obj = ShowDot1xAllDetails(device = self.dev1)
        parsed = obj.parse()
        self.assertEqual(parsed, self.parsed_output_2)

    def test_empty_output(self):
        self.dev2 = Mock(**self.empty_output)
        obj = ShowDot1xAllDetails(device = self.dev2)
        with self.assertRaises(SchemaEmptyParserError):
            parsed = obj.parse()


if __name__ == '__main__':
    unittest.main()