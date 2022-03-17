from pyats.topology.loader import load   # loader of testbed
from pprint import pprint

# I load my testbed file
testbed = load('./testbed/pod1617.yml')

# connection to all devices
testbed.connect(log_stdout=False)

# parse 'show interface status' of all the testbed
output = testbed.parse('show interface status')

# pretty printer
pprint(output)

# disconnect
testbed.disconnect()
