from pyats.easypy import run 
from pyats.topology import loader # for the testbed

def main(runtime):

    runtime.job.name = 'VXLAN EVPN'

    # this is for statically use a testbed but we can use --testbed-file in the pyats run job args
    testbed_1 = loader.load('../testbed/pod499.yml')
    testbed_2 = loader.load('../testbed/pod1617.yml')

    #run task
    run('VXLAN-EVPN_aetest.py',testbed=testbed_1, runtime = runtime, taskid = 'POD 499')
    run('VXLAN-EVPN_aetest.py',testbed=testbed_2, runtime = runtime, taskid = 'POD 1617')

