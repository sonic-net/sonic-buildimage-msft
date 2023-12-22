from unittest.mock import call
import subprocess

"""
    caclmgrd soc test vector
"""
CACLMGRD_SOC_TEST_VECTOR = [
    [
        "SOC_SESSION_TEST",
        {
            "config_db": {
                "DEVICE_METADATA": {
                    "localhost": {
                        "subtype": "DualToR",
                        "type": "ToRRouter",
                    }
                },
                "MUX_CABLE": {
                    "Ethernet4": {
                        "cable_type": "active-active",
                        "soc_ipv4": "10.10.10.7/32",
                    }
                },
                "VLAN_INTERFACE": {
                    "Vlan1000|10.10.10.3/24": {
                        "NULL": "NULL",
                    }
                },
                "LOOPBACK_INTERFACE": {
                    "Loopback3|10.10.10.10/32": {
                        "NULL": "NULL",
                    }
                },
                "FEATURE": {
                },
            },
            "expected_subprocess_calls": [
                call('iptables -t nat -A POSTROUTING --destination 10.10.10.7 --source 10.10.10.18 -j SNAT --to-source 10.10.11.18', shell=True, universal_newlines=True, stdout=-1)
                ],
            "popen_attributes": {
                'communicate.return_value': ('output', 'error'),
            },
            "call_rc": 0,
        }
    ]
]


CACLMGRD_SOC_TEST_VECTOR_EMPTY = [
    [
        "SOC_SESSION_TEST",
        {
            "config_db": {
                "DEVICE_METADATA": {
                    "localhost": {
                        "subtype": "DualToR",
                        "type": "ToRRouter",
                    }
                },
                "MUX_CABLE": {
                    "Ethernet4": {
                        "cable_type": "active-active",
                        "soc_ipv4": "10.10.11.7/32",
                    }
                },
                "VLAN_INTERFACE": {
                    "Vlan1000|10.10.10.3/24": {
                        "NULL": "NULL",
                    }
                },
                "LOOPBACK_INTERFACE": {
                    "Loopback3|10.10.10.10/32": {
                        "NULL": "NULL",
                    }
                },
                "FEATURE": {
                },
            },
            "expected_subprocess_calls": [],
            "popen_attributes": {
                'communicate.return_value': ('output', 'error'),
            },
            "call_rc": 0,
        }
    ]
]
