#!/usr/bin/python3
from modules.native_yang_restconf_VLANs import *
from modules.native_yang_restconf_L3VNIs import *
from modules.native_yang_restconf_L2VNIs import *
from modules.native_yang_restconf_L2_interfaces import *

#---------------------------------------------------------------------------------------------------------
# Variables
#---------------------------------------------------------------------------------------------------------

leaves = [ { 'name' : 'Leaf-111' , 'IP' : '10.60.9.123', 'port' : '20111', 'username' : 'admin', 'password' : 'cisco123'},
           { 'name' : 'Leaf-112' , 'IP' : '10.60.9.123', 'port' : '20112', 'username' : 'admin', 'password' : 'cisco123'},
           { 'name' : 'Leaf-113' , 'IP' : '10.60.9.123', 'port' : '20113', 'username' : 'admin', 'password' : 'cisco123'}
          ]

Leaf_111 = [ { 'name' : 'Leaf-111' , 'IP' : '10.60.9.123', 'port' : '20111', 'username' : 'admin', 'password' : 'cisco123'} ]
Leaf_112 = [ { 'name' : 'Leaf-112' , 'IP' : '10.60.9.123', 'port' : '20112', 'username' : 'admin', 'password' : 'cisco123'} ]
Leaf_113 = [ { 'name' : 'Leaf-113' , 'IP' : '10.60.9.123', 'port' : '20113', 'username' : 'admin', 'password' : 'cisco123'} ]


#---------------------------------------------------------------------------------------------------------
# Main
#---------------------------------------------------------------------------------------------------------
if __name__ == '__main__':


  # add_VLAN(leaves, 100, 'Production', 100000)
  # add_VRF(leaves, 'Production', 100000)
  # add_VRF_to_BGP(leaves, 'Production')
  # add_L3VNI_SVI(leaves, 100, 'Production')
  # add_L3VNI_to_NVE(leaves, 100000)

  # add_VLAN(leaves, 101, 'Production-servers-100101', 100101)
  # add_L2VNI_SVI(leaves, 101, 'Production', 'Production-servers-100101', '10.101.0.254/24')
  # add_L2VNI_to_NVE(leaves, 100101)

  # add_VLAN(leaves, 102, 'Production-servers-100102', 100102)
  # add_L2VNI_SVI(leaves, 102, 'Production', 'Production-servers-100102', '10.102.0.254/24')
  # add_L2VNI_to_NVE(leaves, 100102)

  # add_VPC_port_channel(Leaf_111, 31, '*** To ESX-1 ***', '101,102', 'eth1/31')
  # add_VPC_port_channel(Leaf_112, 31, '*** To ESX-1 ***', '101,102', 'eth1/31')

  # add_switchport_interface(Leaf_113, 'eth1/1', '*** To ESX-4 ***', '101,102')


  delete_L2VNI_from_NVE(leaves, 100101)
  delete_L2VNI_SVI(leaves, 101)
  delete_VLAN(leaves, 101)

  delete_L2VNI_from_NVE(leaves, 100102)
  delete_L2VNI_SVI(leaves, 102)
  delete_VLAN(leaves, 102)

  delete_VRF_from_BGP(leaves, 'Production')
  delete_L3VNI_from_NVE(leaves, 100000)
  delete_L3VNI_SVI(leaves, 100)
  delete_VLAN(leaves, 100)
  delete_VRF(leaves, 'Production')
  
  remove_member_from_port_channel(Leaf_111, 'eth1/31', 31)
  remove_member_from_port_channel(Leaf_112, 'eth1/31', 31)
  reset_interface(Leaf_111, 'eth1/31')
  reset_interface(Leaf_112, 'eth1/31')
  reset_interface(Leaf_113, 'eth1/1')
  delete_VPC_port_channel(Leaf_111, 31)
  delete_VPC_port_channel(Leaf_112, 31)

