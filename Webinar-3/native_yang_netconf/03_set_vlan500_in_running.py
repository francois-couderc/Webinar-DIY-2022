#!/usr/bin/python3
from ncclient import manager

session = manager.connect(host='10.60.9.123', port=40111, username='admin', password='cisco123',
                    hostkey_verify=False, device_params={'name': 'nexus'},
                    look_for_keys=False, allow_agent=False)

rpc_call = '''
<config>
  <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">    
    <bd-items>
      <bd-items>
        <BD-list>
          <fabEncap>vlan-500</fabEncap>
          <accEncap>vxlan-500</accEncap>
          <name>Vlan500-Configured-in-netconf-with-ncclient</name>
        </BD-list>
      </bd-items>
    </bd-items>
  </System>
</config>
               '''

reply = session.edit_config(rpc_call, target="running")
print(reply)