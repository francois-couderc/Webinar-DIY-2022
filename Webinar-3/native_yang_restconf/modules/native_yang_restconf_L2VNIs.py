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
# Add a L2VNI SVI
#---------------------------------------------------------------------------------------------------------
def add_L2VNI_SVI(devices, VLAN_ID, VRF, description, IPDG):
  for device in devices:
    # URL
    URL = 'http://' + device['IP'] + ':' + device['port'] + '/restconf/data/Cisco-NX-OS-device:System'

    # payload
    payload = {
      "hmm-items": {
        "fwdinst-items": {
          "if-items": {
            "FwdIf-list": [
              {
                "id": "vlan" + str(VLAN_ID),
                "mode": "anycastGW"
              }
            ]
          }
        }
      },
      "ipv4-items": {
        "inst-items": {
          "dom-items": {
            "Dom-list": [
              {
                "name": VRF,
                "if-items": {
                  "If-list": [
                    {
                      "id": "vlan" + str(VLAN_ID),
                      "addr-items": {
                        "Addr-list": [
                          {
                            "addr": IPDG,
                            "type": "primary"
                          }
                        ]
                      }
                    }
                  ]
                }
              }
            ]
          }
        }
      },
      "icmpv4-items": {
        "inst-items": {
          "dom-items": {
            "Dom-list": [
              {
                "name": VRF,
                "if-items": {
                  "If-list": [
                    {
                      "ctrl": "port-unreachable",
                      "id": "vlan" + str(VLAN_ID)
                    }
                  ]
                }
              }
            ]
          }
        }
      },
      "intf-items": {
        "svi-items": {
          "If-list": [
            {
              "adminSt": "up",
              "descr": "*** " + description + " L2VNI ***",
              "id": "vlan" + str(VLAN_ID),
              "mtu": "9216",
              "rtvrfMbr-items": {
                "tDn": "/System/inst-items/Inst-list[name='" + VRF + "']"
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
      print('[' + device['name'] +'] - L2VNI SVI ' + str(VLAN_ID) + ' (*** ' + description + ' L2VNI ***) with IPDG ' + IPDG + ' for VRF ' + VRF + ' added' )


#---------------------------------------------------------------------------------------------------------
# Delete a L3VNI SVI
#---------------------------------------------------------------------------------------------------------
def delete_L2VNI_SVI(devices, VLAN_ID):
  for device in devices:
    # URL
    URL = 'http://' + device['IP'] + ':' + device['port'] + '/restconf/data/Cisco-NX-OS-device:System/intf-items/svi-items/If-list=vlan' + str(VLAN_ID)

    # Restconf DELETE
    response = requests.request('DELETE', URL, headers=headers, auth=(device['username'], device['password']))

    # debug
    # print(URL)
    # print(response.status_code)
    if response.status_code == 204:
      print('[' + device['name'] +'] - L2VNI SVI ' + str(VLAN_ID) + ' deleted' )


#---------------------------------------------------------------------------------------------------------
# Add L2VNI to NVE interface
#---------------------------------------------------------------------------------------------------------
def add_L2VNI_to_NVE(devices, VNI_ID):
  for device in devices:
    # URL
    URL = 'http://' + device['IP'] + ':' + device['port'] + '/restconf/data/Cisco-NX-OS-device:System'

    # payload
    payload = {
      "eps-items": {
        "epId-items": {
          "Ep-list": [
            {
              "epId": "1",
              "nws-items": {
                "vni-items": {
                  "Nw-list": [
                    {
                      "isLegacyMode": "false",
                      "vni": str(VNI_ID)
                    }
                  ]
                }
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
      print('[' + device['name'] +'] - L2VNI ' + str(VNI_ID) + ' added to NVE interface' )


#---------------------------------------------------------------------------------------------------------
# Delete L2VNI from NVE interface
#---------------------------------------------------------------------------------------------------------
def delete_L2VNI_from_NVE(devices, VNI_ID):
  for device in devices:
    # URL
    URL = 'http://' + device['IP'] + ':' + device['port'] + '/restconf/data/Cisco-NX-OS-device:System/eps-items/epId-items/Ep-list=1/nws-items/vni-items/Nw-list=' +str(VNI_ID)
    
    # Restconf DELETE
    response = requests.request('DELETE', URL, headers=headers, auth=(device['username'], device['password']))

    # debug
    # print(URL)
    # print(response.status_code)
    if response.status_code == 204:
      print('[' + device['name'] +'] - L2VNI ' + str(VNI_ID) + ' removed from NVE interface' )