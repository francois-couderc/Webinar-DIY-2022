from pyats.topology import loader   # loader of testbed
import time

# I load my testbed file
testbed = loader.load('./testbed/pod499.yml')

# intiate time calculation
start_time = time.time()

# connection to all devices
testbed.connect()

print('****************************************************************************')

for device in testbed.devices: 
    #check if connected
    state = 'connected' if testbed.devices[device].is_connected() else 'not connected'
    print(f'{testbed.devices[device].name} is {state}' )

print('****************************************************************************')
print(f'Execution time for {len(testbed.devices)} devices == {str(time.time() - start_time)} seconds')
print('****************************************************************************')


testbed.disconnect()