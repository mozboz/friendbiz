import unittest
from commands import botCommands
from friendBizApiTests import friendBizTest
import parsing
from testData import setupUsersAndTransactions, setupUsers

__author__ = 'james'


class testFriendBizParsing(friendBizTest):

    def testCommandParsing(self):
        botname = 'friendbiz'
        tweet = 'test5 appl mandarin'
        twitterData = {}
        twitterData['text'] = '@' + botname + ' ' + tweet
        twitterData['user'] = {}
        twitterData['user']['screen_name'] = 'blobby914'
        config = self.getConfig(botname)

        event = parsing.event(twitterData, config)
        assert event.isCommand == True
        assert event.command == 'test5'
        assert event.params == ['appl', 'mandarin']
        assert event.sender == 'blobby914'

    def testEchoCommand(self):
        self.command._dispatch("echo", ["ping","this","back"], "bishbosh")

        assert len(self.fakeTwitter.updateStatusCalls) == 1
        assert self.fakeTwitter.updateStatusCalls[0] == 'Hi @bishbosh, you said: ping this back'

    def testStatusCommand(self):
        u1, u2, u3, t1 = setupUsersAndTransactions(self.session, self.config)
        h = "someguy"
        self.command._dispatch("status", [u1.handle], h)
        assert self.fakeTwitter.updateStatusCalls[0] == '@' + h +', @' + u1.handle + ' is not owned. Their price is 1, they have 100 credits and own 2 players'
        self.command._dispatch("status", [u2.handle], h)
        assert self.fakeTwitter.updateStatusCalls[1] == '@' + h +', @' + u2.handle + ' is owned by @' + u1.handle + '. Their price is 1, they have 100 credits and own 0 players'
        self.command._dispatch("status", [u3.handle], h)
        assert self.fakeTwitter.updateStatusCalls[2] == '@' + h +', @' + u3.handle + ' is owned by @' + u1.handle + '. Their price is 1, they have 100 credits and own 0 players'
        # test with extra @ on front, output should be same
        self.command._dispatch("status", ['@' + u3.handle], h)
        assert self.fakeTwitter.updateStatusCalls[3] == '@' + h +', @' + u3.handle + ' is owned by @' + u1.handle + '. Their price is 1, they have 100 credits and own 0 players'

    def testBuyCommandNotOwner(self):
        u1, u2, u3 = setupUsers(self.session, self.config)
        self.command._dispatch("buy", [u2.handle], u3.handle)
        assert self.fakeTwitter.updateStatusCalls[0] == '@' + u3.handle + ', congrats! You bought @' + u2.handle + ' from @' + u1.handle + ' for ' + str(self.config['startingPrice'])

    def testBuyCommandNotOwned(self):
        u1, u2, u3 = setupUsers(self.session, self.config)
        self.command._dispatch("buy", [u1.handle], u3.handle)
        print "foo" +  self.fakeTwitter.updateStatusCalls[0]
        assert self.fakeTwitter.updateStatusCalls[0] == '@' + u3.handle + ', congrats! You bought @' + u1.handle + ' for ' + str(self.config['startingPrice'])

    def testBuyCommandCantBuyYourself(self):
        u1, u2, u3 = setupUsers(self.session, self.config)
        self.command._dispatch("buy", [u1.handle], u1.handle)
        assert self.fakeTwitter.updateStatusCalls[0] == '@' + u1.handle + ', you can\'t buy yourself ;)'

    def testBuyCommandAlreadyOwner(self):
        u1, u2, u3 = setupUsers(self.session, self.config)
        self.command._dispatch("buy", [u2.handle], u1.handle)
        assert self.fakeTwitter.updateStatusCalls[0] == '@' + u1.handle + ', you already own @' + u2.handle

    def getFakeIncomingTweet(self, botname, command):
        return {"created_at":"Thu Jan 14 21:31:18 +0000 2016",
                  "id":687748850279444480,"id_str":"687748850279444480","text":'@' + botname + ' ' + command,
                  "source":"\u003ca href=\"http:\/\/twitter.com\" rel=\"nofollow\"\u003eTwitter Web Client\u003c\/a\u003e",
                  "truncated":False,"in_reply_to_status_id":'null',"in_reply_to_status_id_str":"null","in_reply_to_user_id":4806590788,
                  "in_reply_to_user_id_str":"4806590788","in_reply_to_screen_name":"friendbiz",
                  "user":{"id":4806590788,"id_str":"4806590788","name":"zzo","screen_name":"friendbiz","location":'null',"url":'null',"description":'null',"protected":False,"verified":False,"followers_count":0,"friends_count":0,"listed_count":0,"favourites_count":0,"statuses_count":11,"created_at":"Thu Jan 14 18:26:16 +0000 2016","utc_offset":-28800,"time_zone":"Pacific Time (US & Canada)","geo_enabled":False,"lang":"en-gb","contributors_enabled":False,"is_translator":False,"profile_background_color":"F5F8FA","profile_background_image_url":"","profile_background_image_url_https":"","profile_background_tile":False,"profile_link_color":"2B7BB9","profile_sidebar_border_color":"C0DEED","profile_sidebar_fill_color":"DDEEF6","profile_text_color":"333333","profile_use_background_image":True,"profile_image_url":"http:\/\/abs.twimg.com\/sticky\/default_profile_images\/default_profile_6_normal.png","profile_image_url_https":"https:\/\/abs.twimg.com\/sticky\/default_profile_images\/default_profile_6_normal.png","default_profile":True,"default_profile_image":True,"following":'null',"follow_request_sent":'null',"notifications":'null'},
                  "geo":'null',"coordinates":'null',"place":'null',"contributors":'null',"is_quote_status":False,"retweet_count":0,"favorite_count":0,"entities":{"hashtags":[],"urls":[],"user_mentions":[{"screen_name":"friendbiz","name":"zzo","id":4806590788,"id_str":"4806590788","indices":[0,10]}],"symbols":[]},"favorited":False,"retweeted":False,"filter_level":"low","lang":"en","timestamp_ms":"1452807078319"}


    def getConfig(self, botname):
        config = {}
        config['botname'] = botname
        return config


if __name__ == "__main__":
    unittest.main()