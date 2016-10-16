#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# IPSender: simple application to send the public IP by e-mail.
# Designed to run automatically (like a service).
# Jordi Castelló.
#
import smtplib, urllib2, json, base64
from email.mime.text import MIMEText


def send_mail(language):
    """ Send an email with the IP from machine, all data values
        are extracted from "mail.json" file. """
    # Extract JSON file data:
    with open('mail.json') as json_file:
        data = json.load(json_file)
    # data:
    user = data['login']['user']
    password = data['login']['pass']
    password = base64.b64decode(password)  # Decode password
    sender = data['sender']
    receivers = data['receivers']
    server = data['smtp']
    port = data['smtport']
    server = server + ':' + port  # Concatenate server and port
    pubip = extract_public_ip()  # Obtain public IP
    msg = data['language'][language]['message'] + pubip
    server = smtplib.SMTP(server)
    server.starttls()
    server.login(user, password)
    for i in range(len(receivers)):
        mime_message = MIMEText(msg.encode('utf-8'), "plain", 'utf-8')
        mime_message["From"] = sender
        mime_message["To"] = receivers[i]
        mime_message["Subject"] = data['language'][language]['subject']
        print receivers[i]
        print type(mime_message)
        print mime_message.as_string()
        server.sendmail(sender, str(receivers[i]), mime_message.as_string())
    server.quit()


def extract_public_ip():
    """ Extract public IP with external web server """
    sock = urllib2.urlopen('http://checkip.dyndns.com/')
    public_ip = sock.read()
    sock.close()
    public_ip = public_ip.split(': ')[-1]
    public_ip = public_ip.split('</body>')[0]
    return public_ip


if __name__ == "__main__":
    LANGUAGE = "en"  # Set desired language (ensure that exists in the JSON file).
    send_mail(LANGUAGE)
