#!/usr/bin/python3
from ncclient import manager

session = manager.connect(host='10.60.9.123', port=40111, username='admin', password='cisco123',
                    hostkey_verify=False, device_params={'name': 'nexus'},
                    look_for_keys=False, allow_agent=False)

reply = session.commit()
print(reply)