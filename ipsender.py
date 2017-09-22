#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# IPSender: simple application to send the public IP by e-mail.
# Designed to run automatically (like a service).
# Jordi Castelló.
#
import smtplib
import urllib2
import sys
import platform
import base64
import getopt
import getpass
from email.mime.text import MIMEText
from parsers.Configuration import Configuration
from parsers.Message import Message
from tools.Obfuscator import Obfuscator

# Configuration constants
LANGUAGE = 'en'  # Set desired language (ensure that exists in the JSON file).
CONFIGURATION_FILE = './data/config.json'
MESSAGE_FILE = './data/message.json'


def main(args):
    if len(args) > 1:   # If there aren't arguments execute normal script.
        try:
            opts, args = getopt.getopt(args[1:], "c", ["configure"])
            for o, a in opts:
                if o in ('-c', '--configure'):
                    configure()
        except getopt.GetoptError as err:
            print str(err)
            sys.exit(2)
    else:
        send_mail(LANGUAGE)


def send_mail(language):
    """ Send an email with the IP from machine, all data values
        are extracted from "mail.json" file. """
    # Extract JSON file data:
    configuration = Configuration(CONFIGURATION_FILE)
    message = Message(MESSAGE_FILE, language)
    # Extract password
    cpassword = base64.b64decode(configuration.password)
    key = base64.b64decode(configuration.key)
    obf = Obfuscator(cpassword, key)    # Decrypt password
    password = str(obf.cpassword)       # Get decrypted password string
    # Concatenate server and port
    server = configuration.server + ':' + configuration.port
    # Obtain information from computer
    user = getpass.getuser()
    # platform.uname() = (system, node, release, version, machine, processor)
    platform_info = platform.uname()
    public_ip = extract_public_ip() 		# Obtain public IP
    msg = message.name + platform_info[1]
    msg += '\n' + message.user + user
    msg += '\n' + message.os + platform_info[0]
    msg += '\n' + message.version + platform_info[2]
    msg += '\n' + message.release + platform_info[3]
    msg += '\n' + message.machine + platform_info[4]
    msg += '\n' + message.processor + platform_info[5]
    msg += '\n\n' + message.ip + public_ip
    # Formatting e-mail:
    mime_message = MIMEText(msg, "plain")
    mime_message["From"] = configuration.sender
    mime_message["To"] = configuration.receiver
    mime_message["Subject"] = message.subject
    # Sending e-mail:
    server = smtplib.SMTP(server)
    server.starttls()
    server.login(configuration.user, password)
    server.sendmail(configuration.sender, configuration.receiver,
                     mime_message.as_string())
    server.quit()


def extract_public_ip():
    """ Extract public IP with external web server """
    sock = urllib2.urlopen('http://checkip.dyndns.com/')
    public_ip = sock.read()
    sock.close()
    public_ip = public_ip.split(': ')[-1]
    public_ip = public_ip.split('</body>')[0]
    return public_ip


def configure():
    """ Create the config.json file needed. This method is called
        when the script is executed with '-c' or '--configure' argument """
    config = Configuration(CONFIGURATION_FILE)
    config.configure()

if __name__ == "__main__":
    main(sys.argv)
