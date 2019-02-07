from selenium import webdriver
from selenium.webdriver.common import action_chains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import yaml
import ipaddress
import sys


class Dock:

    def __init__(self, config_file):
        self.ip_related =[]
        self.name = ''
        self.agency = ''
        self.location = ''
        self.dock_login = ''
        self.dock_passwd = ''
        self.dynamic = ''
        self.ecom_url = ''
        self.ecom_login = ''
        self.ecom_passwd = ''
        self.ip_address = ''
        self.netmask = ''
        self.gateway_ip = ''
        self.dns_server_1 = ''
        self.dns_server_2 = ''
        self.config_file = config_file    

        self.driver = webdriver.Chrome()    
        self.action = action_chains.ActionChains(self.driver)
        
    def read_config(self):
       
        try:
            with open(self.config_file, 'r') as f:
                settings = yaml.safe_load(f)
        except yaml.YAMLError:
            print("Error in configuration file:", exc)
        f.close()

        self.name = settings['name']
        self.location = settings['location']
        self.dock_login = settings['dock_login']
        self.dock_passwd = settings['dock_passwd']
        self.dynamic = settings['dynamic']
        self.ecom_url = settings['ecom_url']
        self.ecom_login = settings['ecom_login']
        self.ecom_passwd = settings['ecom_passwd']
        self.ip_address = settings['ip_address']
        self.netmask = settings['netmask']
        self.gateway_ip = settings['gateway_ip']
        self.dns_server_1 = settings['dns_server_1']
        if (settings['dns_server_2']) is not None:
            self.dns_server_2 = settings['dns_server_2']
            self.ip_related.append(dns_server_2)
        
        self.ip_related = self.ip_related + [self.ip_address, self.netmask, self.gateway_ip, self.dns_server_1]    
           
        
    def validate_ip_addresses(self):
        address = ""
        for address in self.ip_related:
            ip = ipaddress.ip_address(address)
        return True

    def get_status(self):
        self.driver.get('http://' + self.dock_login + ':' + self.dock_passwd + '@10.10.1.1/index.html')

    def configure_network(self):

        self.driver.get('http://' + self.dock_login + ':' + self.dock_passwd + '@10.10.1.1/secure/network.html')

        if not self.dynamic: 
            self.wait = WebDriverWait(self.driver, 30)
            self.static_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'ui-corner-right')))
            self.driver.implicitly_wait(30)
            # self.action.move_to_element(self.static_button).click(self.static_button)
            self.static_button.click()
            self.ip_address_text = self.wait.until(EC.element_to_be_clickable((By.NAME,'network.wan.ipaddr'))) 
            self.ip_address_text.clear()
            self.ip_address_text.send_keys(self.ip_address)
            self.driver.find_element_by_name('network.wan.ipaddr').clear()
            self.driver.find_element_by_name('network.wan.ipaddr').send_keys(self.ip_address)
            self.driver.find_element_by_name('network.wan.netmask').clear()
            self.driver.find_element_by_name('network.wan.netmask').send_keys(self.netmask)
            self.driver.find_element_by_name('network.wan.gateway').clear()
            self.driver.find_element_by_name('network.wan.gateway').send_keys(self.gateway_ip)
            self.driver.find_element_by_name('network.wan.dns[0]').clear()
            self.driver.find_element_by_name('network.wan.dns[0]').send_keys(self.dns_server_1)
            self.driver.save_screenshot('screenshot.png')
            self.driver.find_element_by_id('btnSave').click()
        else:
            self.dhcp_button = self.driver.find_element_by_class_name('ui-corner-left')
            self.driver.implicitly_wait(10)
            self.action.move_to_element(self.dhcp_button).click(self.dhcp_button)
            self.driver.find_element_by_id('btnSave').click()            

    def configure_admin(self):

        self.driver.get('http://' + self.dock_login + ':' + self.dock_passwd + '@10.10.1.1/secure/admin.html')
        self.driver.find_element_by_name('etm.etm.name').clear()
        self.driver.find_element_by_name('etm.etm.name').send_keys(self.name)
        self.driver.find_element_by_name('etm.etm.location').clear()
        self.driver.find_element_by_name('etm.etm.location').send_keys(self.location)
        self.driver.find_element_by_id('btnSave').click()
    
    def reset_registration(self):
        self.driver.get('http://' + self.dock_login + ':' + self.dock_passwd + '@10.10.1.1/secure/ops.html')
        wait = WebDriverWait(self.driver, 10)
        btnResetReg = wait.until(EC.element_to_be_clickable((By.ID, "btnResetReg")))
        btnResetReg.click()
    
    def configure_ecom(self):
        self.driver.get('http://' + self.dock_login + ':' + self.dock_passwd + '@10.10.1.1/secure/ops.html')
        wait = WebDriverWait(self.driver, 10)
        self.driver.find_element_by_id('ecom_domain').send_keys(self.ecom_url)
        self.driver.find_element_by_name('etm.admin.username').send_keys(self.ecom_login)
        self.driver.find_element_by_name('etm.admin.password').send_keys(self.ecom_passwd)
        btnSave = wait.until(EC.element_to_be_clickable((By.ID, "btnSave")))
        btnSave.click()