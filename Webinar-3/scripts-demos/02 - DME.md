# NX-API REST SDK

DME : Data Management Engine

MIT : Management Information Tree
Hierarchical way
Each node in the MIT represents a managed object or group of objects.

Every managed object in the system can be identified by a unique distinguished name (DN)

The NX-API-REST API operates in forgiving mode, which means that missing attributes are substituted with default values (if applicable)

The API is also atomic. If multiple MOs are being configured, and any of the MOs cannot be configured, the API stops its operation. It returns the configuration to its prior state, stops the API operation that listens for API requests, and returns an error code.


## Read

### Sandbox -> Visore

TopSystem -> bdEntity -> sys/bd/bd-[vlan-3600]
Check des attributs du Vlan 3600
Objects du Vlan 3600

show vlan internal info all

Query 1:
sys/bd/bd-[vlan-3600]

Query 2:
l2BD
fabEncap == vlan-3600

### POSTMAN


#### XML
http://10.60.9.123:20111/api/node/mo/sys/bd/bd-[vlan-3600].xml

DME - Login

http://10.60.9.123:20111/api/node/mo/sys/bd/bd-[vlan-3600].xml?rsp-subtree=full


#### JSON

http://10.60.9.123:20111/api/node/mo/sys/bd/bd-[vlan-3600].json

http://10.60.9.123:20111/api/node/mo/sys/bd/bd-[vlan-3600].json?rsp-subtree=full


#### BGP Example

Visore -> Sys / BGP

Postman : http://10.60.9.123:20111/api/node/mo/sys/bgp.json?rsp-subtree=full


## Write

###

Sandbox

vlan 200
  vn-segment 200000

Convert with DN

Send


{
  "topSystem": {
    "attributes": {
      "dn": "sys",
      "rn": "sys"
    },
    "children": [
      {
        "bdEntity": {
          "attributes": {
            "dn": "sys/bd",
            "rn": "bd"
          },
          "children": [
            {
              "l2BD": {
                "attributes": {
                  "accEncap": "vxlan-200000",
                  "dn": "sys/bd/bd-[vlan-200]",
                  "fabEncap": "vlan-200",
                  "name": "TEST",
                  "rn": "bd-[vlan-200]"
                }
              }
            }
          ]
        }
      }
    ]
  }
}

POSTMAN : 

DELETE http://10.60.9.123:20111/api/node/mo/sys/bd/bd-[vlan-200].json



### Conversion DME model to CLI

Sandbox
    NXAPI-REST (DME)
    model
{
  "topSystem": {
    "children": [
      {
        "bdEntity": {
          "children": [
            {
              "l2BD": {
                "attributes": {
                  "accEncap": "vxlan-300000",
                  "fabEncap": "vlan-300",
                  "name": "Configured_with_DME"
                }
              }
            }
          ]
        }
      }
    ]
  }
}




### Documentation

https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/sw/93x/progammability/guide/b-cisco-nexus-9000-series-nx-os-programmability-guide-93x/b-cisco-nexus-9000-series-nx-os-programmability-guide-93x_chapter_0101110.html

https://developer.cisco.com/site/nxapi-dme-model-reference-api/

https://developer.cisco.com/docs/cisco-nexus-3000-and-9000-series-nx-api-rest-sdk-user-guide-and-api-reference-release-9-2x/