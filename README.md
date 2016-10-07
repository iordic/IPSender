# IPSender
Simple commandline tool to send public ip through e-mail. Thought to run as service.

## How to use?
* Configure "mail.json" with your login credentials.
	* Password requires base64 encoding, use codepass.py for this and encode your password.
	![codepass](/img/screenshot.png)
* Set receiver address where program sends the IP.
* If you aren't using gmail, change smtp config.

## TO DO
- [ ] Send e-mails to multiple addresses.
- [ ] Use encryption for the password field.
- [ ] PEP8 Style?
