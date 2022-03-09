#!/usr/bin/python3
import requests
import json

headers = { 
  'Content-Type': 'application/yang.data+json',
  'Accept': 'application/yang.data+json',
  'Cache-Control': 'no-cache'
  }

URL = 'http://10.60.9.123:20115/restconf/data/openconfig-network-instance:network-instances/network-instance=default/protocols'

payload = '''
{
  "protocol": [
    {
      "identifier": "BGP",
      "name": "bgp",
      "bgp": {
        "neighbors": {
          "neighbor": [
            {
              "neighbor-address": "1.1.1.14",
              "config": {
                "peer-group": "overlay_local_spines"
              }
            }
          ]
        }
      }
    }
  ]
}
'''

response = requests.request('PATCH', URL, headers=headers, data=payload, auth=('admin', 'cisco123'))

print(response.status_code)
print(response.text)
