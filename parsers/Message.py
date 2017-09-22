import json


class Message:
    def __init__(self, f, lang='en'):
        with open(f) as json_file:
            data = json.load(json_file)
        language_position = self.check_language(lang, data)
        if language_position < 0:
            self.language = 'en'
            language_position = 0
        else:
            self.language = lang
        self.subject = data['messages'][language_position]['text']['subject']
        self.ip = data['messages'][language_position]['text']['ip']
        self.user = data['messages'][language_position]['text']['user']
        self.name = data['messages'][language_position]['text']['name']
        self.os = data['messages'][language_position]['text']['os']
        self.version = data['messages'][language_position]['text']['version']
        self.release = data['messages'][language_position]['text']['release']
        self.machine = data['messages'][language_position]['text']['machine']
        self.processor = data['messages'][language_position]['text']['processor']

    def check_language(self, lang, data):
        """ Check if language exists on json file. If exists
            return the language position. If not return -1. """
        for i in range(0, len(data['messages'])):
            if data['messages'][i]['lang'] == lang:
                return i
        return -1
