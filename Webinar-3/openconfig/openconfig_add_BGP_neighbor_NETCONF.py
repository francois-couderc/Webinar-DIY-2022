#!/usr/bin/python3
from ncclient import manager

device = {"ip": "10.60.9.123", "port": "40115", "platform": "nexus",}

session = manager.connect(host=device['ip'], port=device['port'], username='admin', password='cisco123',
                    hostkey_verify=False, device_params={'name': device['platform']},
                    look_for_keys=False, allow_agent=False)

rpc_call = '''
<config>
    <network-instances xmlns="http://openconfig.net/yang/network-instance">
        <network-instance>
            <name>default</name>
            <protocols>
                <protocol>
                    <identifier>BGP</identifier>
                    <name>bgp</name>
                    <bgp>
                        <neighbors>
                            <neighbor>
                                <neighbor-address>1.1.1.13</neighbor-address>
                                <config>
                                    <neighbor-address>1.1.1.13</neighbor-address>
                                    <peer-group>overlay_local_spines</peer-group>
                                </config>
                            </neighbor>
                        </neighbors>
                    </bgp>
                </protocol>
            </protocols>
        </network-instance>
    </network-instances>
</config>
            '''

# Apply the config change
reply = session.edit_config(rpc_call, target="running")
print(reply)