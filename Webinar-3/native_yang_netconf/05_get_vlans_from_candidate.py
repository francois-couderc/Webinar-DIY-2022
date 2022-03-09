#!/usr/bin/python3
from ncclient import manager

session = manager.connect(host='10.60.9.123', port=40111, username='admin', password='cisco123',
                    hostkey_verify=False, device_params={'name': 'nexus'},
                    look_for_keys=False, allow_agent=False)

rpc_call = '''
<System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">    
  <bd-items>
    <bd-items/>
  </bd-items>
</System>
               '''

reply = session.get_config('candidate', filter=('subtree', rpc_call))
print(reply)