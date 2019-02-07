#!/usr/bin/env python

import dock
import logging
import time
import argparse

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO)
   
    logging.info('Reading Dock configuration')
    parser = argparse.ArgumentParser(description=
    'Configure an Axon Dock for use with Evidence.com or Axon Commander')
 
    parser.add_argument('-f', '--file', required=True,type=str,help=' YAML configuration file')
    args= parser.parse_args() #create an object having name and age as attributes)
 
    filename = args.file
   
    dock = dock.Dock(filename)
    print(filename)
    dock.read_config()

    logging.info('Configure Dock administrative information')
    dock.configure_admin()

    logging.info('Waiting for Dock availability')
    time.sleep(15)

    # Check that the IP addresses in configuration files are correct, otherwise abort
    dock.validate_ip_addresses()
    
    logging.info('Configuring Dock IP Address: %s' % dock.ip_address)
    dock.configure_network()
    
    logging.info('Waiting for Dock availability')
    time.sleep(20)
    
    logging.info('Reset Dock registration with e.com')
    dock.reset_registration()
    # wait some time to allow the reset procedure to finish
    logging.info('Waiting for Dock availability')
    time.sleep(40)
    
    logging.info('Configuring Dock registration to ' + dock.ecom_url)
    dock.configure_ecom()
    time.sleep(20)

    logging.info('Checking Dock status')
    dock.get_status()
    time.sleep(20)
    logging.info('Dock Configuration done.')












