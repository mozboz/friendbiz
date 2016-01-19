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
from helpers import getDbString
import parsing
from twitterUtils import userExists

consumer_key="ckGuKbZGHiWy4OlT5eziWwjYV"
consumer_secret="Jad2glvZLxWo7OBLNn3yLuCMFxSGgeNcbVV2mfdRvV49SQcyFg"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="4806590788-7FIv0Mo3TSKgeDxGc9koQU8LGPJCn4CT22C1BgD"
access_token_secret="cseVvqTZsH6GClR4Yvd1NZJnO8jkJs0Qyb0aVReGdOpev"

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
                self.command.dispatch(event.command, event.params, event.sender)
            else:
                print("Not command")
                print(twitterJson)

        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':

    config = {"startingBalance":100, "startingPrice":1, "historyLength":10, "botname": "friendbiz"}
    platform = "prod"

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    twitterAPI = API(auth)

    engine = create_engine(getDbString(platform), pool_recycle=3600)
    dbSessionMaker = sessionmaker(bind=engine)

    friendBizAPI = friendBizAPI(dbSessionMaker, config)

    l = StdOutListener(config, twitterAPI, friendBizAPI)
    stream = Stream(auth, l)
    stream.userstream()
