# DockBot
> An attempt to automate Axon Dock configuration

The Dock python class (in ```dock.py```) contains the logic to automatically configure an Axon Dock to work with Evidence.com or Axon Commander. 

## Installing / Getting started

1. Install Chrome browser on your platform
2. Install python3 see (https://realpython.com/installing-python/)
3. Install Chrome WebDriver ( see http://chromedriver.chromium.org/home)
4. Install Selenium and Pyyaml libraries 

	```$ pip3 install < requirements.txt```

### Initial Configuration

The Axon Dock configuration parameters must be described in an YAML file, which will be read by the main program.
This repository includes ```config.yaml``` as an example.

The configuration parameters are self-explanatory:

- name -  *Name assigned to the Axon Dock*
- location - *Location of the Dock inside the agency (i.e. “Armory Room”)
- dock_login - *login username for the Dock*
- dock_passwd - *login password for the Dock*
- dynamic - *Whether the Dock uses static or dynamic (DHCP) IP assignment - Value must be True or False*
- ip_address - *IP address of the Dock*
- netmask - *IP netmaks*
- gateway_ip - *Default gateway IP address* 
- dns_server_1 - *First DNS Server to be queried*
- dns_server_2 - *Second DNS Server to be queried*
- ecom_url:  - “URL of the evidence.com or Axon Commander instance*
- ecom_login: - *Evidence.com or Axon Commander administrator login username*
- ecom_passwd: - *Evidence.com or Axon Commander administrator login password*


## Usage Example

1. Connect the dock LAN port to your PC ethernet port. 
2. Configure PC’s ethernet IP address on the network 10.10.1.x/24 (10.10.1.1 is the Dock default address)
3. Execute test program ```dock_config.py```

	```$ python3 dock_config.py -f config.yaml```

This sample program will open a Chrome bowser window and will configure the dock with the parameters described in the ```config.yaml``` YAML file.


