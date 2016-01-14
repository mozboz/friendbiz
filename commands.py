
class event:

    def __init__(self, twitterData, config):
        self.config = config
        self.isCommand = False
        self.command = ''
        self.preProcess(twitterData)

    def preProcess(self, twitterData):
#        print('foo')
#        print(self.config['botname'])
#        print twitterData['text'][0:2]
        # print twitterData['text'][0:len(self.config['botname'])+2].lower()
        if twitterData['text'][0:len(self.config['botname'])+2].lower() == ''.join(['@',self.config['botname'],' ']).lower():
            self.command = twitterData['text'][len(self.config['botname'])+2:]
            self.isCommand = True

