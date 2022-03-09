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
# Add a VPC port-channel
#---------------------------------------------------------------------------------------------------------
def add_VPC_port_channel(devices, PO_ID, description, VLANs_ID, member):
  for device in devices:
    # URL
    URL = 'http://' + device['IP'] + ':' + device['port'] + '/restconf/data/Cisco-NX-OS-device:System'

    # payload
    payload = {
      "vpc-items": {
        "inst-items": {
          "dom-items": {
            "if-items": {
              "If-list": [
                {
                  "id": str(PO_ID),
                  "rsvpcConf-items": {
                    "tDn": "/System/intf-items/aggr-items/AggrIf-list[id='po" + str(PO_ID) + "']"
                  }
                }
              ]
            }
          }
        }
      },
      "stp-items": {
        "inst-items": {
          "if-items": {
            "If-list": [
              {
                "id": "po" + str(PO_ID),
                "mode": "trunk"
              }
            ]
          }
        }
      },
      "intf-items": {
        "phys-items": {
          "PhysIf-list": [
            {
              "adminSt": "up",
              "descr": description,
              "id": member,
              "layer": "Layer2",
              "userCfgdFlags": "admin_layer,admin_mtu,admin_state"
            }
          ]
        },
        "aggr-items": {
          "AggrIf-list": [
            {
              "adminSt": "up",
              "descr": description,
              "id": "po" + str(PO_ID),
              "layer": "Layer2",
              "mode": "trunk",
              "mtu": "9216",
              "pcMode": "active",
              "trunkVlans": VLANs_ID,
              "userCfgdFlags": "admin_layer,admin_mtu,admin_state",
              "rsmbrIfs-items": {
                "RsMbrIfs-list": [
                  {
                    "isMbrForce": "true",
                    "tDn": "/System/intf-items/phys-items/PhysIf-list[id='" + member + "']"
                  }
                ]
              }
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
      print('[' + device['name'] +'] - VPC Port-channel ' + str(PO_ID) + ' added with member ' + member + ' and VLANs ' + VLANs_ID)


#---------------------------------------------------------------------------------------------------------
# Delete a VPC port-channel
#---------------------------------------------------------------------------------------------------------
def delete_VPC_port_channel(devices, PO_ID):
  for device in devices:

    # Part 1 : VPC deletion from port-channel
    # URL
    URL = 'http://' + device['IP'] + ':' + device['port'] + '/restconf/data/Cisco-NX-OS-device:System/vpc-items/inst-items/dom-items/if-items/If-list=' + str(PO_ID)

    # Restconf DELETE
    response = requests.request('DELETE', URL, headers=headers, auth=(device['username'], device['password']))

    # debug
    # print(URL)
    # print(response.status_code)
    if response.status_code == 204:
      print('[' + device['name'] +'] - VPC ' + str(PO_ID) + ' removed from port-channel ' + str(PO_ID) )

    # Part 2 : port-channel deletion
    # URL
    URL = 'http://' + device['IP'] + ':' + device['port'] + '/restconf/data/Cisco-NX-OS-device:System/intf-items/aggr-items/AggrIf-list=po' + str(PO_ID) 

    # Restconf DELETE
    response = requests.request('DELETE', URL, headers=headers, auth=(device['username'], device['password']))

    # debug
    # print(URL)
    # print(response.status_code)
    if response.status_code == 204:
      print('[' + device['name'] +'] - Port-channel ' + str(PO_ID) + ' deleted' )


#---------------------------------------------------------------------------------------------------------
# Remove member from port-channel
#---------------------------------------------------------------------------------------------------------
def remove_member_from_port_channel(devices, interface, PO_ID):
  for device in devices:
    # URL
    URL = 'http://' + device['IP'] + ':' + device['port'] + '/restconf/data/Cisco-NX-OS-device:System/intf-items/aggr-items/AggrIf-list=po' + str(PO_ID) + "/rsmbrIfs-items"

    # Restconf DELETE
    response = requests.request('DELETE', URL, headers=headers, auth=(device['username'], device['password']))

    # debug
    # print(URL)
    # print(response.status_code)
    if response.status_code == 204:
      print('[' + device['name'] +'] - interface ' + interface + ' detached from port-channel ' + str(PO_ID))


#---------------------------------------------------------------------------------------------------------
# Reset an interface to factory defaults
#---------------------------------------------------------------------------------------------------------
def reset_interface(devices, interface):
  for device in devices:
    # URL
    URL = 'http://' + device['IP'] + ':' + device['port'] + '/restconf/data/Cisco-NX-OS-device:System'

    # payload
    payload = {
      "intf-items": {
        "phys-items": {
          "PhysIf-list": [
            {
              "id": interface,
              "adminSt": "down",
              "descr": "",
              "layer": "Layer3",
              "mtu": "1500"
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
      print('[' + device['name'] +'] - interface ' + interface + ' reseted to factory defaults' )


#---------------------------------------------------------------------------------------------------------
# Add a switchport trunk interface with appropriate vlans
#---------------------------------------------------------------------------------------------------------
def add_switchport_interface(devices, interface, description, VLANs_ID):
  for device in devices:
    # URL
    URL = 'http://' + device['IP'] + ':' + device['port'] + '/restconf/data/Cisco-NX-OS-device:System'

    # payload
    payload = {
    "intf-items": {
      "phys-items": {
        "PhysIf-list": [
          {
            "adminSt": "up",
            "descr": description,
            "id": interface,
            "layer": "Layer2",
            "mode": "trunk",
            "mtu": "9216",
            "trunkVlans": VLANs_ID,
            "userCfgdFlags": "admin_layer,admin_mtu,admin_state"
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
      print('[' + device['name'] +'] - switchport trunk interface ' + interface + ' added with vlans ' + VLANs_ID)