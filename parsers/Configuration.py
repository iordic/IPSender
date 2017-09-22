import json
import os
import getpass
import base64
from tools.Obfuscator import Obfuscator


class Configuration:
    def __init__(self, f):
        self.file = f
        if os.path.isfile(self.file):
            self.load_data()
        else:
            raise Exception('File not found: config.json, try using -c parameter.')

    def load_data(self):
        """ Load the json data in the config.json file. """
        try:
            with open(self.file, 'r') as json_file:
                self.data = json.load(json_file)
            self.user = self.data['login']['user']
            self.password = self.data['login']['password']
            self.key = self.data['login']['key']
            self.sender = self.data['sender']
            self.receiver =self.data['receiver']
            self.protocol = self.data['protocol']
            self.server = self.data['server']
            self.port = self.data['port']
        except IOError as err:
            print "Can't open file"

    def update_file(self):
        """ Replaces config.json file with the new data. """
        with open(self.file, 'w') as json_file:
            json.dump(self.data, json_file)

    def configure(self):
        """ Configuration method for creating the config.json file or replace it. """
        with open('./data/config_template.json', 'r') as template:
            json_data = json.load(template)
        print '\nLogin configuration:'
        print '===================='
        json_data['login']['user'] = raw_input('Enter username: ')
        password = getpass.getpass('Enter password: ')
        o = Obfuscator(password)
        json_data['login']['password'] = base64.b64encode(o.cpassword)
        json_data['login']['key'] = base64.b64encode(o.key)
        del o
        print '\nE-mail options:'
        print '================='
        json_data['sender'] = raw_input('Enter the sender address: ')
        json_data['receiver'] = raw_input('Enter the receiver address: ')
        print '\nServer options:'
        print '==============='
        server = raw_input('Enter the server address (blank for smtp.gmail.com): ')
        if server != '':
            json_data['server'] = server
        protocol = raw_input('Enter the protocol (blank for smtp): ')
        if protocol != '':
            json_data['protocol'] = protocol
        port = raw_input('Enter the port (blank for 587): ')
        if port != '':
            json_data['port'] = port
        self.data = json_data
        self.update_file()
