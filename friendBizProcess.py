from __future__ import absolute_import, print_function
import json

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Stream


# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from commands import botCommands
from friendBizAPI import friendBizAPI
import parsing
import configuration
from twitterUtils import userExists
from urllib3.exceptions import ReadTimeoutError

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """

    def __init__(self, config, twitterAPI, friendBizAPI):
        self.config = config
        self.twitterAPI = twitterAPI
        self.friendBizAPI = friendBizAPI
        self.command = botCommands(self.twitterAPI, self.friendBizAPI)

    def on_data(self, twitterJson):
        twitterData = json.loads(twitterJson)

        if 'text' in twitterData:
        # get a context object with useful information appended, and unuseful information removed.
            event = parsing.event(twitterData, self.config)
            if event.isCommand:
                print("Attempting to dispatch command " + event.command + " from " + event.sender)
                self.command._dispatch(event.command, event.params, event.sender)
            else:
                print("Not command")
                print(twitterData['text'] + "\n" + twitterData['user']['screen_name'] + ' : ' + twitterData['created_at'])

        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':

    config = {"startingBalance":100, "startingPrice":1, "historyLength":10, "botname": "friendbiz"}
    platform = "prod"

    auth = OAuthHandler(configuration.friendBizConfig.twitterAPICredentials['consumer_key'], configuration.friendBizConfig.twitterAPICredentials['consumer_secret'])
    auth.set_access_token(configuration.friendBizConfig.twitterAPICredentials['access_token'], configuration.friendBizConfig.twitterAPICredentials['access_token_secret'])
    twitterAPI = API(auth)

    engine = create_engine(configuration.friendBizConfig.dbConnectionString[platform], pool_recycle=3600)
    dbSessionMaker = sessionmaker(bind=engine)

    friendBizAPI = friendBizAPI(dbSessionMaker, config)

    l = StdOutListener(config, twitterAPI, friendBizAPI)
    stream = Stream(auth, l)
    while True:
        try:
            stream.userstream()
        except ReadTimeoutError as e:
            print(e)