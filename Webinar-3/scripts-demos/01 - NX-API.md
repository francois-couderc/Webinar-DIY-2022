# NX-API

restore FOUNDATIONS
no nxapi

## Read


```
Leaf-111# show lldp neighbors
Capability codes:
  (R) Router, (B) Bridge, (T) Telephone, (C) DOCSIS Cable Device
  (W) WLAN Access Point, (P) Repeater, (S) Station, (O) Other
Device ID            Local Intf      Hold-time  Capability  Port ID
APIC1                Eth1/1          120                    f07f.0653.0fdd
Leaf-112             Eth1/49         120        BR          Ethernet1/49
Spine-11             Eth1/51         120        BR          Ethernet1/1
Spine-12             Eth1/52         120        BR          Ethernet1/1
Total entries displayed: 4
```



```
Leaf-111# show lldp neighbors | json-pretty
{
    "neigh_hdr": "neigh_hdr",
    "TABLE_nbor": {
        "ROW_nbor": [
            {
                "chassis_type": "Locally Assigned",
                "chassis_id": "APIC1",
                "l_port_id": "Eth1/1",
                "hold_time": "120",
                "system_capability": null,
                "enabled_capability": "!",
                "port_type": "Mac Address",
                "port_id": "f07f.0653.0fdd",
                "mgmt_addr_type": "IPV4",
                "mgmt_addr": "10.1.0.1",
                "mgmt_addr_ipv6_type": "Address not advertised",
                "mgmt_addr_ipv6": "not advertised"
            },
            {
                "chassis_type": "Locally Assigned",
                "chassis_id": "Leaf-112",
                "l_port_id": "Eth1/49",
                "hold_time": "120",
                "system_capability": "BR",
                "enabled_capability": "BR",
                "port_type": "Interface Name",
                "port_id": "Ethernet1/49",
                "mgmt_addr_type": "IPV4",
                "mgmt_addr": "192.168.123.112",
                "mgmt_addr_ipv6_type": "802",
                "mgmt_addr_ipv6": "003a.9c25.44c8"
            },
            {
                "chassis_type": "Locally Assigned",
                "chassis_id": "Spine-11",
                "l_port_id": "Eth1/51",
                "hold_time": "120",
                "system_capability": "BR",
                "enabled_capability": "BR",
                "port_type": "Interface Name",
                "port_id": "Ethernet1/1",
                "mgmt_addr_type": "IPV4",
                "mgmt_addr": "192.168.123.121",
                "mgmt_addr_ipv6_type": "802",
                "mgmt_addr_ipv6": "780c.f036.210e"
            },
            {
                "chassis_type": "Locally Assigned",
                "chassis_id": "Spine-12",
                "l_port_id": "Eth1/52",
                "hold_time": "120",
                "system_capability": "BR",
                "enabled_capability": "BR",
                "port_type": "Interface Name",
                "port_id": "Ethernet1/1",
                "mgmt_addr_type": "IPV4",
                "mgmt_addr": "192.168.123.122",
                "mgmt_addr_ipv6_type": "802",
                "mgmt_addr_ipv6": "780c.f0a2.04a0"
            }
        ]
    },
    "neigh_count": "4"
}
```

feature nxapi

```
Leaf-111# show nxapi
nxapi enabled
NXAPI timeout 10
HTTPS Listen on port 443
Certificate Information:
    Issuer:   /C=US/ST=CA/L=San Jose/O=Cisco Systems Inc./OU=dcnxos/CN=nxos
    Expires:  Mar  4 16:37:04 2022 GMT
```

nxapi http port 80

```
Leaf-111# show nxapi
nxapi enabled
NXAPI timeout 10
HTTP Listen on port 80
HTTPS Listen on port 443
Certificate Information:
    Issuer:   /C=US/ST=CA/L=San Jose/O=Cisco Systems Inc./OU=dcnxos/CN=nxos
    Expires:  Mar  4 16:37:04 2022 GMT
```


Sandbox Leaf-111
  NXAPI-CLI
  json
  cli_show
  show lldp neighbors -> Send

Show Outputs Schema

Récupérer le code python3

Fichier get_lldp_neighbors.py :
```
#!/usr/bin/python3
import requests
import json
from pprint import pprint

switchuser='admin'
switchpassword='cisco123'

url='http://10.60.9.123:20111/ins'

myheaders={'content-type':'application/json'}

payload={
  "ins_api": {
    "version": "1.0",
    "type": "cli_show",
    "chunk": "0",
    "sid": "sid",
    "input": "show lldp neighbors",
    "output_format": "json"
  }
}

response = requests.post(url, data=json.dumps(payload), headers=myheaders, auth=(switchuser,switchpassword)).json()

print(response)
```

formater le résultat json dans Code

print(response["ins_api"]["outputs"]["output"]["body"]["TABLE_nbor"]["ROW_nbor"])

for neighbor in response["ins_api"]["outputs"]["output"]["body"]["TABLE_nbor"]["ROW_nbor"]:
  print("interface", '{0: <7}'.format(neighbor["l_port_id"]), ":", neighbor["chassis_id"])

## Write

Sandbox Leaf-111
  NXAPI-CLI
  json
  cli_conf
vlan 100
  vn-segment 100000

sh run vlan

no vlan 100

Postman
  Environnements
    Globals
    Leaf-111

New Request :
POST http://{{jumphost}}:{{port}}/ins
Authorization : Basic Auth {{username}} / {{password}}
Body Raw/JSON :
{
  "ins_api": {
    "version": "1.0",
    "type": "cli_conf",
    "chunk": "0",
    "sid": "sid",
    "input": "vlan 100 ;  vn-segment 100000 ; name Created-with-NXAPI-CLI",
    "output_format": "json"
  }
}
Headers -> Content-Type : application/json

Send


Documentation :

https://developer.cisco.com/docs/cisco-nexus-9000-series-nx-api-cli-reference-release-9-3x/

https://www.cisco.com/c/en/us/support/switches/nexus-9000-series-switches/products-programming-reference-guides-list.html

https://www.cisco.com/c/dam/en/us/td/docs/switches/datacenter/nexus9000/sw/open_nxos/programmability/guide/Programmability_Open_NX-OS.pdf
