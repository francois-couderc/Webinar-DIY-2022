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
# Add a VRF
#---------------------------------------------------------------------------------------------------------
def add_VRF(devices, name, VNI_ID):
  for device in devices:
    # URL
    URL = 'http://' + device['IP'] + ':' + device['port'] + '/restconf/data/Cisco-NX-OS-device:System'

    # payload

    ## Option 1 :
    # VLAN = {}
    # VLAN['encap'] = 'vxlan-' + str(VNI_ID)
    # VLAN['name']  = name

    # Inst_list = []
    # Inst_list.append(VLAN)

    # inst_items = {}
    # inst_items['Inst-list'] = Inst_list

    # payload = {}
    # payload['inst-items'] = inst_items

    ## Option 2 :
    payload = {
      "inst-items": {
        "Inst-list": [
          {
            "encap": "vxlan-" + str(VNI_ID),
            "name": name
          }
        ]
      }
    }

    # Restconf PATCH
    response = requests.request('PATCH', URL, data=json.dumps(payload), headers=headers, auth=(device['username'], device['password']))

    # debug
    # print(URL)
    # print(json.dumps(payload, indent=2))
    # print(response.status_code)
    if response.status_code == 204:
      print('[' + device['name'] +'] - VRF ' + name + ' with L3VNI ' + str(VNI_ID) + ' added' )


#---------------------------------------------------------------------------------------------------------
# Delete a VRF
#---------------------------------------------------------------------------------------------------------
def delete_VRF(devices, name):
  for device in devices:
    # URL
    URL = 'http://' + device['IP'] + ':' + device['port'] + '/restconf/data/Cisco-NX-OS-device:System/inst-items/Inst-list=' + name
    
    # Restconf DELETE
    response = requests.request('DELETE', URL, headers=headers, auth=(device['username'], device['password']))

    # debug
    # print(URL)
    # print(response.status_code)
    if response.status_code == 204:
      print('[' + device['name'] +'] - VRF ' + name + ' deleted' )


#---------------------------------------------------------------------------------------------------------
# Add a L3VNI SVI
#---------------------------------------------------------------------------------------------------------
def add_L3VNI_SVI(devices, VLAN_ID, VRF):
  for device in devices:
    # URL
    URL = 'http://' + device['IP'] + ':' + device['port'] + '/restconf/data/Cisco-NX-OS-device:System'

    # payload
    payload = {
      "ipv4-items": {
        "inst-items": {
          "dom-items": {
            "Dom-list": [
              {
                "name": VRF,
                "if-items": {
                  "If-list": [
                    {
                      "forward": "enabled",
                      "id": "vlan" + str(VLAN_ID)
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
              "descr": "*** " + VRF + " VRF symmetric transit ***",
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
      print('[' + device['name'] +'] - L3VNI SVI ' + str(VLAN_ID) + ' (*** ' + VRF + ' VRF symmetric transit ***) for VRF ' + VRF + ' added' )


#---------------------------------------------------------------------------------------------------------
# Delete a L3VNI SVI
#---------------------------------------------------------------------------------------------------------
def delete_L3VNI_SVI(devices, VLAN_ID):
  for device in devices:
    # URL
    URL = 'http://' + device['IP'] + ':' + device['port'] + '/restconf/data/Cisco-NX-OS-device:System/intf-items/svi-items/If-list=vlan' + str(VLAN_ID)

    # Restconf DELETE
    response = requests.request('DELETE', URL, headers=headers, auth=(device['username'], device['password']))

    # debug
    # print(URL)
    # print(response.status_code)
    if response.status_code == 204:
      print('[' + device['name'] +'] - L3VNI SVI ' + str(VLAN_ID) + ' deleted' )


#---------------------------------------------------------------------------------------------------------
# Add L3VNI to NVE interface
#---------------------------------------------------------------------------------------------------------
def add_L3VNI_to_NVE(devices, VNI_ID):
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
                      "associateVrfFlag": "true",
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
      print('[' + device['name'] +'] - L3VNI ' + str(VNI_ID) + ' added to NVE interface' )


#---------------------------------------------------------------------------------------------------------
# Delete L3VNI from NVE interface
#---------------------------------------------------------------------------------------------------------
def delete_L3VNI_from_NVE(devices, VNI_ID):
  for device in devices:
    # URL
    URL = 'http://' + device['IP'] + ':' + device['port'] + '/restconf/data/Cisco-NX-OS-device:System/eps-items/epId-items/Ep-list=1/nws-items/vni-items/Nw-list=' +str(VNI_ID)
    
    # Restconf DELETE
    response = requests.request('DELETE', URL, headers=headers, auth=(device['username'], device['password']))

    # debug
    # print(URL)
    # print(response.status_code)
    if response.status_code == 204:
      print('[' + device['name'] +'] - L3VNI ' + str(VNI_ID) + ' removed from NVE interface' )


#---------------------------------------------------------------------------------------------------------
# Add VRF configuration to BGP
#---------------------------------------------------------------------------------------------------------
def add_VRF_to_BGP(devices, VRF):
  for device in devices:
    # Get local BGP ASN number
    URL = 'http://' + device['IP'] + ':' + device['port'] + '/restconf/data/Cisco-NX-OS-device:System/bgp-items/inst-items/asn'
    response = requests.request('GET', URL, headers=headers, auth=(device['username'], device['password']))
    ASN = json.loads(response.text)["asn"]

    # URL
    URL = 'http://' + device['IP'] + ':' + device['port'] + '/restconf/data/Cisco-NX-OS-device:System'

    # payload
    payload = {
      "bgp-items": {
        "inst-items": {
          "asn": ASN,
          "dom-items": {
            "Dom-list": [
              {
                "name": VRF,
                "af-items": {
                  "DomAf-list": [
                    {
                      "advertL2vpnEvpn": "enabled",
                      "maxEcmp": "2",
                      "type": "ipv4-ucast"
                    }
                  ]
                }
              }
            ]
          }
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
      print('[' + device['name'] +'] - VRF ' + VRF + ' configuration added to BGP' )


#---------------------------------------------------------------------------------------------------------
# Delete VRF configuration from BGP
#---------------------------------------------------------------------------------------------------------
def delete_VRF_from_BGP(devices, VRF):
  for device in devices:
    # URL
    URL = 'http://' + device['IP'] + ':' + device['port'] + '/restconf/data/Cisco-NX-OS-device:System/bgp-items/inst-items/dom-items/Dom-list=' + VRF
    
    # Restconf DELETE
    response = requests.request('DELETE', URL, headers=headers, auth=(device['username'], device['password']))

    # debug
    # print(URL)
    # print(response.status_code)
    if response.status_code == 204:
      print('[' + device['name'] +'] - VRF ' + VRF + ' configuration removed from BGP' )