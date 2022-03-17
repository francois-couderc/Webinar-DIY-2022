from pyats.easypy import Task
from pyats.topology import loader # for the testbed


def main():

    #fabric pod499
    testbed_1 = loader.load('./testbed/pod499.yml')

    #fabric pod1617
    testbed_2 = loader.load('./testbed/pod1617.yml')

    first_step = Task('first_steps.py')
    VPC_check_testbed1 = Task('VPC_Check.py', testbed=testbed_1)
    VPC_check_testbed2 = Task('VPC_Check.py', testbed=testbed_2)

    first_step.start()
    VPC_check_testbed1.start()
    VPC_check_testbed2.start()
        
    first_step.wait(45)
    VPC_check_testbed1.wait(45)
    VPC_check_testbed2.wait(45)
