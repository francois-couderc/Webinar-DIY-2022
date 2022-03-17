from pyats.topology.loader import load   # aka from genie.testbed import load
from pprint import pprint
from genie.utils import Dq

# I load my testbed file
testbed = load('./testbed/pod499.yml')

# connection to LEAF-101
testbed.devices['LEAF-101'].connect(log_stdout=False)

# three possibilities to retrieve the same information
output1 = testbed.devices['LEAF-101'].execute('show cdp neighbor')
output2 = testbed.devices['LEAF-101'].parse('show cdp neighbor')
output3 = testbed.devices['LEAF-101'].api.get_cdp_neighbors_info()


print('****************************** EXECUTE ******************************')
print(f'type of object : {type(output1)}')
print('*********************************************************************')
pprint(output1)
print('*********************************************************************')
pprint('')
pprint('')
print('******************************* PARSE *******************************')
print(f'type of object : {type(output2)}')
print('*********************************************************************')
pprint(output2)
print('*********************************************************************')
pprint('')
pprint('')
print('******************************** API ********************************')
print(f'type of object : {type(output3)}')
print('*********************************************************************')
pprint(output3)
print('*********************************************************************')
pprint('')
pprint('')
print('******************************* QDict *******************************')
print(f'I just need the \'system name\' of the neighbor')
print('*********************************************************************')
pprint(output2.q.get_values('device_id'))
print('*********************************************************************')


testbed.devices['LEAF-101'].disconnect()
