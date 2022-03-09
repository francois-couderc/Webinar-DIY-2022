#!/usr/bin/env python3
import re
from ncclient import manager

# Context manager keeping ncclient connection alive for the duration of
# the context.
with manager.connect(
    host='10.60.9.123',     # IP address of the XR device in your pod
    port=40111,              # Port to connect to
    username='admin',      # SSH Username
    password='cisco123',  # SSH Password
    hostkey_verify=False   # Allow unknown hostkeys not in local store
) as m:  # Context manager reference, i.e. instance of connected manager
    # The rest of your script code should go here.

    capabilities = []
    # Write each capability to console
    for capability in m.server_capabilities:
        # Print the capability
        print("Capability: %s" % capability)
        # Store the capability list for later.
        capabilities.append(capability)

    # Sort the list alphabetically.
    capabilities = sorted(capabilities)
    # List of modules that we store for use later
    modules = []
    # Iterate server capabilities and extract supported modules.
    for capability in capabilities:
        # Scan the capabilities and extract modules via this regex.
        # i.e., if this was the capability string:
        #   http://www.cisco.com/calvados/show_diag?module=show_diag&revision=2012-03-27
        # then:
        #   show_diag
        # .. would be the module printed.
        # Scan capability string for module
        supported_model = re.search('module=(.*)&', capability)
        # If module found in string, store it.
        if supported_model is not None:
            # Module string was found, store it.
            print("Supported Model: %s" % supported_model.group(1))
            # Store the module for later use.
            modules.append(supported_model.groups(0)[0])
