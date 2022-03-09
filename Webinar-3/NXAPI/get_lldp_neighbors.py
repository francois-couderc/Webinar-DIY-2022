#!/usr/bin/python3
import requests
import json

switchuser='admin'
switchpassword='cisco123'

url='http://10.60.9.123:20111/ins'

myheaders={'content-type':'application/json'}

payload={
  "ins_api": {
    "version": "1.0",
    "type": "cli_show",
    "chunk": "0",
    "sid": "sid",
    "input": "show lldp neighbors",
    "output_format": "json"
  }
}

response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(switchuser,switchpassword)).json()

for neighbor in response["ins_api"]["outputs"]["output"]["body"]["TABLE_nbor"]["ROW_nbor"]:
  print("interface", '{0: <7}'.format(neighbor["l_port_id"]), ":", neighbor["chassis_id"])