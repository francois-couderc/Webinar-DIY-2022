# To get a logger for the script
import logging

# Needed for aetest script
from pyats import aetest
from pyats.topology import loader

# Get your logger for your script
log = logging.getLogger(__name__)

######################
#COMMON SETUP SECTION#
######################
class Common_Setup(aetest.CommonSetup):
    @aetest.subsection
    def Subsection_one(self):
        pass
    @aetest.subsection
    def Subsection_two(self):
        pass           
    @aetest.subsection
    def Subsection_three(self):
        pass  

###################
#TESTCASES SECTION# ORDER
###################

class Testcase_one(aetest.Testcase):
    @aetest.test
    def Test_three(self):
        pass
    @aetest.test
    def Test_one(self):
        pass
    @aetest.cleanup
    def Cleanup(self):
        pass
    @aetest.test
    def Test_two(self):
        pass
    @aetest.setup
    def Setup(self):
        pass

###################
#TESTCASES SECTION# use ASSERT
###################

class Testcase_two(aetest.Testcase):
    @aetest.setup
    def Setup(self):
        pass
    @aetest.test
    def Test_one(self):
        assert 1 == 1
    @aetest.test
    def Test_two(self):
        assert 1 == 2 ; 'la raison'
    @aetest.test
    def Test_three(self):
        x = 1/0
        assert x == 1
    @aetest.cleanup
    def Cleanup(self):
        pass

###################
#TESTCASES SECTION# 
###################

class Testcase_three(aetest.Testcase):
    @aetest.setup
    def Setup(self):
        pass
    @aetest.test
    def Test_Passed(self):
        self.passed("ca passe")
    @aetest.test
    def Test_Passx(self):
        self.passx("ca passe mais pas la prochaine fois")
    @aetest.test
    def Test_Failed(self):
        self.failed("ca ne passe pas")
    @aetest.cleanup
    def Cleanup(self):
        pass

########################
#COMMON CLEANUP SECTION#
########################

class Common_Cleanup(aetest.CommonCleanup):
    @aetest.subsection
    def Subsection_one(self):
        pass
    @aetest.subsection
    def Subsection_two(self):
        pass
    @aetest.subsection
    def Subsection_three(self):
        pass

def main(testbed):
    
    log.setLevel(logging.INFO)
    aetest.main(testbed = testbed)


if __name__ == '__main__':
    testbed = loader.load('./testbed/pod1617.yml')
    main(testbed = testbed)
    