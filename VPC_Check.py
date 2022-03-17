# To get a logger for the script
import logging

# use to troubleshoot dictionnaries
from pprint import pprint

# Needed for aetest script
from pyats import aetest            # Automation Testing
from pyats.topology.loader import load   # loader of testbed
from genie.utils import Dq          # used to find a specific value inside a dictionnary


# Get your logger for your script
log = logging.getLogger(__name__)

# list all outputs for tests
feature_dict = dict()
vpc_dict = dict()

# function to test if the feature is Disabled
def feature_enabled(device, feature):
    return ''.join(Dq(feature_dict).contains(device).contains(feature).contains('1').get_values('state'))=='enabled'

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
    def show_features(self, testbed):
        global feature_dict
        feature_dict = dict(testbed.parse('show feature'))

    # Finally we will take the "show vpc" on the devices where the feature VPC is enabled
    @aetest.subsection
    def show_vpc(self,steps, testbed):
        global vpc_dict        
        
        # test device per device
        for device in feature_dict.keys():
            
            if feature_enabled(device,'vpc'):
                #
                # the feature VPC is enabled 
                with steps.start(f'\'show vpc\' ==> {device}'):
                    vpc_dict[device] = dict(testbed.devices[device].parse('show vpc'))
            else:    
                #
                # the feature VPC is disabled 
                with steps.start(f'no vpc feature ==> {device}') as step:
                    step.skipped('no feature vpc')

###################
#TESTCASES SECTION#
###################
# Testcase name : VPC_Check

@aetest.loop(device=vpc_dict.keys())
class VPC_Check(aetest.Testcase):


    @aetest.test
    def Peer_status(self, device):
        tmp = ''.join(Dq(vpc_dict).contains(device).get_values('vpc_peer_status'))
        self.passed() if 'peer adjacency formed ok' else self.failed(tmp)
            

    @aetest.test
    def Peer_Keepalive_status(self, device):        
        tmp = ''.join(Dq(vpc_dict).contains(device).get_values('vpc_peer_keepalive_status'))
        self.passed() if 'peer is alive' else self.failed(tmp)

    
    @aetest.test
    def Peer_Gateway_status(self, device):        
        tmp = ''.join(Dq(vpc_dict).contains(device).get_values('peer_gateway'))
        self.passed() if tmp == 'Enabled' else self.failed(tmp)
        
    @aetest.test
    def Peer_Link_status(self, device):        
        tmp = ''.join(Dq(vpc_dict).contains(device).get_values('peer_link_port_state'))
        self.passed() if tmp == 'up' else self.failed(tmp)
        
    @aetest.test
    def Type2_Consistency_status(self, device):        
        tmp = ''.join(Dq(vpc_dict).contains(device).get_values('vpc_type_2_consistency_status'))
        self.passed() if tmp == 'success' else self.failed(tmp)


########################
#COMMON CLEANUP SECTION#
########################
class common_cleanup(aetest.CommonCleanup):

    @aetest.subsection
    def disconnect(self, testbed):
        testbed.disconnect()


if __name__ == '__main__':
    
    testbed = load('./testbed/pod499.yml') 
    log.setLevel(logging.INFO)
    aetest.main(testbed = testbed)