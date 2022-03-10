# Openconfig

in bash shell :

cd /bootflash
yum remove mtx-openconfig-all-1.0.0.0-9.3.8.lib32_n9000

## Check current status
labuser@diy:~/DIY/native_yang_netconf$ ./01_get_capabilities.py
Capability: urn:ietf:params:netconf:base:1.0
Capability: urn:ietf:params:netconf:base:1.1
Capability: urn:ietf:params:netconf:capability:writable-running:1.0
Capability: urn:ietf:params:netconf:capability:rollback-on-error:1.0
Capability: urn:ietf:params:netconf:capability:candidate:1.0
Capability: urn:ietf:params:netconf:capability:validate:1.1
Capability: urn:ietf:params:netconf:capability:confirmed-commit:1.1
Capability: urn:ietf:params:netconf:capability:notification:1.0
Capability: urn:ietf:params:netconf:capability:interleave:1.0
Capability: urn:ietf:params:netconf:capability:with-defaults:1.0?basic-mode=report-all
Capability: http://cisco.com/ns/yang/cisco-nx-os-device?revision=2021-08-04&module=Cisco-NX-OS-device

## Install Openconfig models
repository URL : https://devhub.cisco.com/artifactory/open-nxos-agents/9.3-8/x86_64/

copy http://10.60.7.9/bin/nxos/nx9k/mtx-openconfig-all-1.0.0.0-9.3.8.lib32_n9000.rpm bootflash: vrf management

then in bash shell :

cd /bootflash
yum install mtx-openconfig-all-1.0.0.0-9.3.8.lib32_n9000.rpm

## Check current status
bash-4.3# yum list installed | grep mtx
mtx-device.lib32_n9000                 2.0.0.0-9.3.8                 installed
mtx-grpc-agent.lib32_n9000             2.1.0.0-9.3.8                 installed
mtx-infra.lib32_n9000                  2.0.0.0-9.3.8                 installed
mtx-netconf-agent.lib32_n9000          2.0.0.0-9.3.8                 installed
mtx-openconfig-all.lib32_n9000         1.0.0.0-9.3.8                 @/mtx-openconfig-all-1.0.0.0-9.3.8.lib32_n9000
mtx-restconf-agent.lib32_n9000         2.0.0.0-9.3.8                 installed
mtx-telemetry.lib32_n9000              2.0.0.0-9.3.8                 installed

labuser@diy:~/DIY/native_yang_netconf$ ./01_get_capabilities.py
Capability: urn:ietf:params:netconf:base:1.0
Capability: urn:ietf:params:netconf:base:1.1
Capability: urn:ietf:params:netconf:capability:writable-running:1.0
Capability: urn:ietf:params:netconf:capability:rollback-on-error:1.0
Capability: urn:ietf:params:netconf:capability:candidate:1.0
Capability: urn:ietf:params:netconf:capability:validate:1.1
Capability: urn:ietf:params:netconf:capability:confirmed-commit:1.1
Capability: urn:ietf:params:netconf:capability:notification:1.0
Capability: urn:ietf:params:netconf:capability:interleave:1.0
Capability: urn:ietf:params:netconf:capability:with-defaults:1.0?basic-mode=report-all
Capability: http://cisco.com/ns/yang/cisco-nx-os-device?revision=2021-08-04&module=Cisco-NX-OS-device
Capability: http://openconfig.net/yang/acl?revision=2019-11-27&module=openconfig-acl&deviations=cisco-nx-openconfig-acl-deviations
Capability: http://openconfig.net/yang/bfd?revision=2019-10-25&module=openconfig-bfd&deviations=cisco-nx-openconfig-bfd-deviations
Capability: http://openconfig.net/yang/bgp-policy?revision=2019-11-28&module=openconfig-bgp-policy&deviations=cisco-nx-openconfig-bgp-policy-deviations
Capability: http://openconfig.net/yang/interfaces?revision=2017-07-14&module=openconfig-interfaces&deviations=cisco-nx-openconfig-interfaces-deviations
Capability: http://openconfig.net/yang/interfaces/aggregate?revision=2017-07-14&module=openconfig-if-aggregate&deviations=cisco-nx-openconfig-if-aggregate-deviations
Capability: http://openconfig.net/yang/interfaces/ethernet?revision=2017-07-14&module=openconfig-if-ethernet&deviations=cisco-nx-openconfig-if-ethernet-deviations
Capability: http://openconfig.net/yang/interfaces/ip?revision=2018-01-05&module=openconfig-if-ip&deviations=cisco-nx-openconfig-if-ip-deviations
Capability: http://openconfig.net/yang/interfaces/ip-ext?revision=2018-01-05&module=openconfig-if-ip-ext&deviations=cisco-nx-openconfig-if-ip-ext-deviations
Capability: http://openconfig.net/yang/lacp?revision=2018-11-21&module=openconfig-lacp&deviations=cisco-nx-openconfig-lacp-deviations
Capability: http://openconfig.net/yang/lldp?revision=2018-11-21&module=openconfig-lldp&deviations=cisco-nx-openconfig-lldp-deviations
Capability: http://openconfig.net/yang/network-instance?revision=2018-11-21&module=openconfig-network-instance&deviations=cisco-nx-openconfig-network-instance-deviations
Capability: http://openconfig.net/yang/network-instance/policy?revision=2018-11-21&module=openconfig-network-instance-policy&deviations=cisco-nx-openconfig-network-instance-policy-deviations
Capability: http://openconfig.net/yang/ospf-policy?revision=2017-08-24&module=openconfig-ospf-policy&deviations=cisco-nx-openconfig-ospf-policy-deviations
Capability: http://openconfig.net/yang/platform?revision=2019-04-16&module=openconfig-platform&deviations=cisco-nx-openconfig-platform-deviations
Capability: http://openconfig.net/yang/platform/cpu?revision=2018-11-21&module=openconfig-platform-cpu&deviations=cisco-nx-openconfig-platform-cpu-deviations
Capability: http://openconfig.net/yang/platform/fan?revision=2018-11-21&module=openconfig-platform-fan&deviations=cisco-nx-openconfig-platform-fan-deviations
Capability: http://openconfig.net/yang/platform/linecard?revision=2018-11-21&module=openconfig-platform-linecard&deviations=cisco-nx-openconfig-platform-linecard-deviations
Capability: http://openconfig.net/yang/platform/port?revision=2018-11-21&module=openconfig-platform-port&deviations=cisco-nx-openconfig-platform-port-deviations
Capability: http://openconfig.net/yang/platform/psu?revision=2018-11-21&module=openconfig-platform-psu&deviations=cisco-nx-openconfig-platform-psu-deviations
Capability: http://openconfig.net/yang/platform/transceiver?revision=2018-11-25&module=openconfig-platform-transceiver&deviations=cisco-nx-openconfig-platform-transceiver-deviations
Capability: http://openconfig.net/yang/qos?revision=2019-11-28&module=openconfig-qos&deviations=cisco-nx-openconfig-qos-deviations
Capability: http://openconfig.net/yang/relay-agent?revision=2018-11-21&module=openconfig-relay-agent&deviations=cisco-nx-openconfig-relay-agent-deviations
Capability: http://openconfig.net/yang/routing-policy?revision=2018-11-21&module=openconfig-routing-policy&deviations=cisco-nx-openconfig-routing-policy-deviations
Capability: http://openconfig.net/yang/spanning-tree?revision=2019-11-28&module=openconfig-spanning-tree&deviations=cisco-nx-openconfig-spanning-tree-deviations
Capability: http://openconfig.net/yang/system?revision=2019-03-15&module=openconfig-system&deviations=cisco-nx-openconfig-system-deviations
Capability: http://openconfig.net/yang/telemetry?revision=2018-11-21&module=openconfig-telemetry&deviations=cisco-nx-openconfig-telemetry-deviations
Capability: http://openconfig.net/yang/vlan?revision=2018-11-21&module=openconfig-vlan&deviations=cisco-nx-openconfig-vlan-deviations
Supported Model: openconfig-acl
Supported Model: openconfig-bfd
Supported Model: openconfig-bgp-policy
Supported Model: openconfig-if-aggregate
Supported Model: openconfig-if-ethernet
Supported Model: openconfig-if-ip-ext
Supported Model: openconfig-if-ip
Supported Model: openconfig-interfaces
Supported Model: openconfig-lacp
Supported Model: openconfig-lldp
Supported Model: openconfig-network-instance-policy
Supported Model: openconfig-network-instance
Supported Model: openconfig-ospf-policy
Supported Model: openconfig-platform-cpu
Supported Model: openconfig-platform-fan
Supported Model: openconfig-platform-linecard
Supported Model: openconfig-platform-port
Supported Model: openconfig-platform-psu
Supported Model: openconfig-platform-transceiver
Supported Model: openconfig-platform
Supported Model: openconfig-qos
Supported Model: openconfig-relay-agent
Supported Model: openconfig-routing-policy
Supported Model: openconfig-spanning-tree
Supported Model: openconfig-system
Supported Model: openconfig-telemetry
Supported Model: openconfig-vlan

## BGP


curl -u admin:cisco123 -X GET 'http://10.60.9.123:20111/restconf/data/openconfig-interfaces:interfaces/interface=eth1%2f41?content=config'


curl -u admin:cisco123 -X GET 'http://10.60.9.123:20111/restconf/data/openconfig-network-instance:network-instances/network-instance/protocols/protocol/bgp/neighbors'

curl -u admin:cisco123 -X GET 'http://10.60.9.123:20111/restconf/data/openconfig-network-instance:network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor=1.1.1.11'

curl -u admin:cisco123 -X GET 'http://10.60.9.123:20111/restconf/data/openconfig-network-instance:network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor=1.1.1.11?content=config'