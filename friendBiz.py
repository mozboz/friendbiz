from __future__ import absolute_import, print_function
import json

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Stream



# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
import commands

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

    def __init__(self, config, api):
        self.config = config
        self.api = api

    def on_data(self, twitterJson):
        twitterData = json.loads(twitterJson)

        if 'text' in twitterData:
        # get a context object with useful information appended, and unuseful information removed.
            event = commands.event(twitterData, self.config)
            if event.isCommand:
                print(event.command)
                self.api.update_status(event.command)
            else:
                print("Not command")
                print(twitterJson)

        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':

    config = {}
    config['botname'] = 'friendbiz'

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = API(auth)
    api.update_status('foo?')

    l = StdOutListener(config, api)
    stream = Stream(auth, l)
    stream.userstream()
