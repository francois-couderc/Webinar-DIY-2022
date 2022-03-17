# To get a logger for the script
from enum import auto
import logging
from multiprocessing.connection import wait

# use to troubleshoot dictionnaries
from pprint import pprint

# Needed for aetest script
from pyats import aetest            # Automation Testing
from pyats.topology.loader import load   # loader of testbed
from genie.utils import Dq
from pyparsing import line          # used to find a specific value inside a dictionnary

# regular expression
import re

# Get your logger for your script
log = logging.getLogger(__name__)

# list all outputs for tests
show_feature = dict()       # list per device the features
show_vpc = dict()           # if "feature vpc", list per device the "show vpc" output
show_ip_ospf_neighbor = dict() # if "feature ospf", list per device the "show ip ospf neighbor" 
show_ip_ospf_interface = dict() # if "feature ospf", list per device the "show ip ospf interface brief" 
show_bgp_l2vpn_evpn_summary = dict()     # list per device the "show bgp l2vpn evpn summary" 

# function to test if the feature is Disabled
def feature_enabled(device, feature):
    return ''.join(Dq(show_feature).contains(device).contains(feature).contains('1').get_values('state'))=='enabled'

######################
#COMMON SETUP SECTION#
######################
class Common_Setup(aetest.CommonSetup):
    
    # First connection to devices
    @aetest.subsection
    def Connections(self, testbed):
        testbed.connect(log_stdout=False)

    # Second we will retrive the Feature status
    @aetest.subsection
    def list_all_features(self, testbed):
        global show_feature
        show_feature = dict(testbed.parse('show feature'))

    # we will take the "show vpc" on the devices where the feature VPC is enabled
    @aetest.subsection
    def list_vpc_status(self,steps, testbed):
        global show_vpc        

        # test device per device
        for device in show_feature.keys():
            
            if feature_enabled(device,'vpc'):
                #
                # the feature VPC is enabled 
                with steps.start(f'\'show vpc\' ==> {device}'):
                    show_vpc[device] = dict(testbed.devices[device].parse('show vpc'))

            else:    
                #
                # the feature VPC is disabled 
                with steps.start(f'no vpc feature ==> {device}'):
                    pass


# we will take the "show ip ospf neighbor"
    @aetest.subsection
    def list_ospf_status(self,steps, testbed):
        
        # test device per device
        for device in show_feature.keys():
            
            if feature_enabled(device,'ospf'):
                #
                # the feature OSPF is enabled 
                with steps.start(f'\'show ip ospf neighbor\' ==> {device}'):
                    show_ip_ospf_neighbor[device] = dict(testbed.devices[device].parse('show ip ospf neighbors detail'))
                    show_ip_ospf_interface[device] = dict(testbed.devices[device].parse('show ip ospf interface'))

            else:    
                #
                # the feature OSPF is disabled 
                with steps.start(f'no ospf feature ==> {device}'):
                    self.failed('ospf must be enabled on this device')
    
    # we will take the "show ip ospf neighbor"
    @aetest.subsection
    def list_bgp_l2vpn_summary(self,steps, testbed):
        
        # test device per device
        for device in show_feature.keys():
            
            if feature_enabled(device,'bgp'):
                #
                # the feature BGP is enabled 
                with steps.start(f'\'show bgp l2vpn evpn summary\' ==> {device}'):
                    show_bgp_l2vpn_evpn_summary[device] = dict(testbed.devices[device].parse('show bgp l2vpn evpn summary'))

            else:    
                #
                # the feature BGP is disabled 
                with steps.start(f'no bgp feature ==> {device}'):
                    self.failed('BGP must be enabled on this device')

###################
#TESTCASES SECTION#
###################
# Testcase name : VPC_Global_Check

@aetest.loop(device=show_vpc.keys())
class VPC_Global_Check(aetest.Testcase):    
        
    @aetest.test
    def Peer_status(self, device):
        tmp = ''.join(Dq(show_vpc).contains(device).get_values('vpc_peer_status'))
        self.passed() if tmp == 'peer adjacency formed ok' else self.failed(tmp)
            

    @aetest.test
    def Peer_Keepalive_status(self, device):        
        tmp = ''.join(Dq(show_vpc).contains(device).get_values('vpc_peer_keepalive_status'))
        self.passed() if tmp == 'peer is alive' else self.failed(tmp)

    @aetest.test
    def L3_Peer_Router_status(self, device):        
        tmp = ''.join(Dq(show_vpc).contains(device).get_values('operational_l3_peer_router'))
        self.passed() if tmp == 'Enabled' else self.passx(f'Feature is {tmp}, it should be Enabled')
    
    @aetest.test
    def Peer_Gateway_status(self, device):        
        tmp = ''.join(Dq(show_vpc).contains(device).get_values('peer_gateway'))
        self.passed() if tmp == 'Enabled' else self.failed(tmp)

    @aetest.test
    def Type2_Consistency_status(self, device):        
        tmp = ''.join(Dq(show_vpc).contains(device).get_values('vpc_type_2_consistency_status'))
        self.passed() if tmp == 'success' else self.failed(tmp)
        
    @aetest.test
    def Peer_Link_status(self, device):        
        tmp = ''.join(Dq(show_vpc).contains(device).get_values('peer_link_port_state'))
        self.passed() if tmp == 'up' else self.failed(tmp)

    @aetest.test
    def Counter_status(self, device, steps):        
        # retrieve auto-recovery ligne
        tmp = ''.join(Dq(show_vpc).contains(device).get_values('vpc_auto_recovery_status'))
        auto_recovery = re.match(r'(\w+), timer is (\w+).\(timeout = (\w+)s(.*)?\)',tmp)
        auto_recovery_state = auto_recovery.group(1)
        auto_recovery_timer = auto_recovery.group(2)
        auto_recovery_timer_conf = auto_recovery.group(3)
        

        # gather the delay_restore
        tmp = ''.join(Dq(show_vpc).contains(device).get_values('vpc_delay_restore_status'))        
        delay_restore = re.match(r'Timer is (\w+).\(timeout = (\w+)s(.*)?\)',tmp)
        delay_restore_timer = delay_restore.group(1)
        delay_restore_timer_conf = delay_restore.group(2)

        # gather the delay_restore_svi
        tmp = ''.join(Dq(show_vpc).contains(device).get_values('vpc_delay_restore_svi_status'))        
        delay_restore_svi = re.match(r'Timer is (\w+).\(timeout = (\w+)s(.*)?\)',tmp)
        delay_restore_svi_timer = delay_restore_svi.group(1)
        delay_restore_svi_timer_conf = delay_restore_svi.group(2)
        
        ## Autorecovery timer
        # check if autorecovery is Enabled
        with steps.start(f'auto-recovery is {auto_recovery_state.upper()}',continue_=True) as step:
            step.failed('auto-recovery must be enabled') if auto_recovery_state != 'Enabled' else step.passed()
        # check if the timer is Off (no reload + Peer-keppalive issue)
        with steps.start(f'auto-recovery timer is {auto_recovery_timer.upper()}',continue_=True) as step:
            step.failed('auto-recovery timer has started please wait for the end of the timer') if auto_recovery_timer != 'off' else step.passed()
        # check if the timer is configured at 360
        with steps.start(f'auto-recovery timer is {auto_recovery_timer_conf}',continue_=True) as step:
            step.failed('auto-recovery timer must be set at 360') if auto_recovery_timer_conf != '360' else step.passed()
        
        ## delay restore timer
        # check if the timer is Off (no delay restore timer started)
        with steps.start(f'delay-restore == {delay_restore_timer.upper()}',continue_=True) as step:
            step.failed('delay-restore timer has started, we need to wait') if delay_restore_timer != 'off' else step.passed()
        
        # check the timer configuration for delay-restore (180s)
        with steps.start(f'delay-restore == {delay_restore_timer_conf}',continue_=True) as step:
            step.failed('delay-restore should be set at 180') if delay_restore_timer_conf != '180' else step.passed()
        
        ## delay-restore-svi timer
        # check if the timer is Off (no delay restore svi timer started)
        with steps.start(f'delay-restore-svi timer is {delay_restore_svi_timer.upper()}',continue_=True) as step:
            step.failed('delay-restore-svi timer has started, we need to wait') if delay_restore_svi_timer != 'off' else step.passed()
        
        # check the timer configuration for delay-restore-svi (10s)
        with steps.start(f'delay-restore-svi == {delay_restore_svi_timer_conf}',continue_=True) as step:
            step.failed('delay-restore should be set at 10') if delay_restore_svi_timer_conf != '10' else step.passed()
        
    
    @aetest.test
    def VPC_status(self, device, steps):
        #gather all the VPC ID fron the 'device'
        vpc = Dq(show_vpc).contains(device).contains('vpc')

        # retrieve all the VPC IDs
        vpc_id_dict = dict(vpc.contains('vpc_id'))

        # loop to check all the VPC of the device
        for line in vpc_id_dict:
            #first need to retrieve the ID
            id = vpc_id_dict[line]
            
            # with the ID it will be possible to retrieve the port state, consistency state and consistency status
            vpc_consistency_status = ''.join(vpc.contains(id).get_values('vpc_consistency_status'))
            vpc_port_state = ''.join(vpc.contains(id).get_values('vpc_port_state'))
            vpc_consistency = ''.join(vpc.contains(id).get_values('vpc_consistency'))

            # let s test first with the port state
            with steps.start(f'VPC{id} state == {vpc_port_state}',continue_=True) as step:
                step.failed(f'VPC{id} is {vpc_port_state}') if vpc_port_state != 'up' else step.passed()

            # let's test the consistency is there any type 1 or 2 inconsistency
            with steps.start(f'VPC{id} consistency == {vpc_consistency}',continue_=True) as step:
                step.failed(f'VPC{id}: {vpc_consistency_status}') if vpc_consistency != 'success' else step.passed()


###################
#TESTCASES SECTION#
###################
# Testcase name : OSPF_Check

@aetest.loop(device=show_ip_ospf_interface.keys())
class OSPF_Check(aetest.Testcase):    

    @aetest.test
    def OSPF_area_check(self, device, steps):
        # seeking the OSPF adjacencies on all other area than 0.0.0.0
        tmp = dict(Dq(show_ip_ospf_neighbor).contains(device).contains('state'))
        
        
        for item in tmp:
            interface = item[10]    # take the interface number
            area = item[8]          # take the area number

            # list all the interface and check            
            with steps.start(f' {interface} in OSPF area {area} ',continue_=True) as step:
                step.passed() if area == '0.0.0.0' else step.failed(f'please configure the interface {interface} in area 0.0.0.0')
                
            

    @aetest.test
    def OSPF_Neighbor_status(self, device, steps):
        tmp = dict(Dq(show_ip_ospf_neighbor).contains(device).contains('state'))
        full = dict(Dq(show_ip_ospf_neighbor).contains(device).contains('state').contains('full'))
        vpc_device = dict(Dq(show_vpc).contains(device))

        pprint(vpc_device)
        # check number of adjacencies
        with steps.start(f'{len(full)}/{len(tmp)} adjacenc(y|ies)',continue_=True) as step:
            if len(full) == 0 and len(tmp) == 0:
                step.failed('No adjacency configured, please configure at least')            
            elif len(full) == 0 and len(tmp) != 0:
                step.failed('There is no adjacency up, underlay will not work')
            elif len(full) == 1 and len(tmp) == 1:
                step.passx('Only one adjacency, there is a SPOF')
            elif len(full) == 1 and len(tmp) > 1:
                step.passx('Only one adjacency full, there is a SPOF, please troubleshoot the non-full interface')
            else:
                step.passed()
            


        for item in tmp:
            interface = item[10]
            state = tmp[item] 
            
            # list all the interfaces not in 'FULL' state
            with steps.start(f'{interface} == state {state.upper()} ',continue_=True) as step:
                step.passed() if state == 'full' else step.failed(f'please check configuration of {interface} on both sides')
                

    @aetest.test
    def OSPF_interfaces_timers(self, device, steps):
        tmp = Dq(show_ip_ospf_interface).contains(device)

        # retrieve all the dictionnaries
        transmit_delay = dict(tmp.contains('transmit_delay') )
        wait_interval = dict(tmp.contains('wait_interval'))
        hello_interval = dict(tmp.contains('hello_interval'))
        retransmit_interval = dict(tmp.contains('retransmit_interval'))

        for ligne in transmit_delay:
            interface = ligne[10]
            timer = transmit_delay[ligne]
            
            # Check if tranmit == 1
            with steps.start(f'{interface} transmit delay : {timer}',continue_=True) as step:
                if timer != 1:
                    step.failed('Transmit delay must be set at 1')
                    
        for ligne in wait_interval:
            interface = ligne[10]
            timer = wait_interval[ligne]
            
            # Check if tranmit == 40
            with steps.start(f'{interface} wait_interval : {timer}',continue_=True) as step:
                if timer != 40:
                    step.failed('Transmit delay must be set at 40')
            
        for ligne in hello_interval:
            interface = ligne[10]
            timer = hello_interval[ligne]
            
            # Check if hello == 10
            with steps.start(f'{interface} hello : {timer}',continue_=True) as step:
                if timer != 10:
                    step.failed('Hello must be set at 10')

        for ligne in retransmit_interval:
            interface = ligne[10]
            timer = retransmit_interval[ligne]
            
            # Check if retransmit == 5
            with steps.start(f'{interface} retransmit : {timer}',continue_=True) as step:
                if timer != 5:
                    step.failed('Hello must be set at 5')

    @aetest.test
    def OSPF_interfaces_status(self, device, steps):
        tmp = Dq(show_ip_ospf_interface).contains(device)
        reason = ''
        
        line_protocol = dict(tmp.contains('line_protocol'))
        enable = dict(tmp.not_contains('bfd').contains('enable')) 
        
        # check the configuration first if administratively down
        for ligne in enable:
            interface = ligne[10]   
            up = enable[ligne] # True = enable or False = disable
            status = 'enable' if up else 'disable'
            with steps.start(f'{interface} is {status}',continue_=True) as step:
                if not up :
                    step.failed(f'{interface} is {status}, please enable it')
        
        # check the line protocol if there is any issue
        for ligne in line_protocol:
            interface = ligne[10]   
            status = line_protocol[ligne]
            with steps.start(f'{interface} is {status}',continue_=True) as step:
                if status != 'up':
                    step.failed(f'{interface} is {status}')
            

###################
#TESTCASES SECTION#
###################
# Testcase name : BGP_Check

@aetest.loop(device=show_bgp_l2vpn_evpn_summary.keys())
class BGP_Check(aetest.Testcase):    

    @aetest.test
    def BGP_peers_check(self, device, steps):
        tmp = Dq(show_bgp_l2vpn_evpn_summary).contains(device)
        
        # state of the peerings
        state = dict(tmp.contains('state'))
        # number of prefix received per peerings
        prefixreceived = dict(tmp.contains('prefixreceived'))
        #number of peerings "established"
        established = dict(tmp.contains('established'))
        
        # check the number of peerings configured
        with steps.start(f'{len(state)} peer(s) configured', continue_=True) as step:
            if len(state) == 1 :
                step.passx('To avoid SPOF please add at least one peering') 
            elif len(state) > 1 :
                step.passed() 
            else:
                step.failed('no peers configured')
            
        # check the number of peerings established
        with steps.start(f'{len(established)}/{len(state)} peering(s) established', continue_=True) as step:
            if len(established) == len(state):
                step.passed()
            elif len(established) == 0:
                step.failed('no peering established')
            else:
                step.passx('one or more peerings not established')
        
        for pref in prefixreceived:
            neighbor = pref[8]

            # check the number of prefix received per peerings    
            with steps.start(f'{prefixreceived[pref]} prefix received from {neighbor}', continue_=True):
                if not isinstance(prefixreceived[pref],int):
                    step.failed('check the peerings')
                elif prefixreceived[pref] == 0:
                    step.passx('no prefix received, configuration is probably missing ?')
                else:
                    step.passed()

             

        
            

 

########################
#COMMON CLEANUP SECTION#
########################
class common_cleanup(aetest.CommonCleanup):

    @aetest.subsection
    def disconnect(self, testbed):
        testbed.disconnect()


if __name__ == '__main__':
    
    testbed = load('../testbed/pod499.yml') 
    log.setLevel(logging.INFO)
    aetest.main(testbed = testbed)