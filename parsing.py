
class event:

    def __init__(self, twitterData, config):
        self.config = config
        self.isCommand = False
        self.command = ''
        self.process(twitterData)

    def process(self, twitterData):
        words = twitterData['text'].split()
        if words[0].lower() == ''.join(['@',self.config['botname']]).lower():
            self.command = words[1]
            self.params = words[2:]
            self.isCommand = True
            self.sender = twitterData['user']['screen_name']

