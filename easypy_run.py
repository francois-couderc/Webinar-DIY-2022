from pyats.easypy import run 
from pyats.topology import loader # for the testbed

def main():

    # this is for statically use a testbed but we can use --testbed-file in the pyats run job args
    testbed_1 = loader.load('./testbed/pod499.yml')

    run('first_steps.py')
    run('VPC_Check.py',testbed=testbed_1)
