import requests
import json


#---------------------------------------------------------------------------------------------------------
# Variables
#---------------------------------------------------------------------------------------------------------
headers = { 
  'Content-Type': 'application/yang.data+json',
  'Accept': 'application/yang.data+json',
  'Cache-Control': 'no-cache'
  }


#---------------------------------------------------------------------------------------------------------
# Add a VLAN
#---------------------------------------------------------------------------------------------------------
def add_VLAN(devices, VLAN_ID, name, VNI_ID):
  for device in devices:
    # URL
    URL = 'http://' + device['IP'] + ':' + device['port'] + '/restconf/data/Cisco-NX-OS-device:System'

    # payload
    payload = {
      "bd-items": {
        "bd-items": {
          "BD-list": [
            {
              "accEncap": "vxlan-" + str(VNI_ID),
              "fabEncap": "vlan-" + str(VLAN_ID),
              "name": name
            }
          ]
        }
      }
    }
    
    # Restconf PATCH
    response = requests.request('PATCH', URL, data=json.dumps(payload), headers=headers, auth=(device['username'], device['password']))

    # debug
    # print(URL)
    # print(json.dumps(payload, indent=2))
    # print(response.status_code)
    if response.status_code == 204:
      print('[' + device['name'] +'] - VLAN ' + str(VLAN_ID) + ' with name ' + name + ' and VNI ' + str(VNI_ID) + ' added' )


#---------------------------------------------------------------------------------------------------------
# Delete a VLAN
#---------------------------------------------------------------------------------------------------------
def delete_VLAN(devices, VLAN_ID):
  for device in devices:
    # URL
    URL = 'http://' + device['IP'] + ':' + device['port'] + '/restconf/data/Cisco-NX-OS-device:System/bd-items/bd-items/BD-list=vlan-' + str(VLAN_ID)
    
    # Restconf DELETE
    response = requests.request('DELETE', URL, headers=headers, auth=(device['username'], device['password']))

    # debug
    # print(URL)
    # print(response.status_code)
    if response.status_code == 204:
      print('[' + device['name'] +'] - VLAN ' + str(VLAN_ID) + ' deleted' )
      
