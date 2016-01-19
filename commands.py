from friendBizAPI import TransactionValues
from friendBizUtils import prettyStatus
from twitterUtils import userExists, rateLimit
from tweepy import TweepError

__author__ = 'james'

# Process command tweeted to the bot
#
# Example command tweeted by someUser
#
#       @botName buy 10 fish
#
# For this command, dispatch will receive (command='buy', params=['10','fish'], sender='someUser')
# Note duplicate whitespace in original tweet intentionally lost
#
# Twitter rate limiting (2400 tweets per day, limited at smaller time increments), means that it is not
# clever to send error messages

class botCommands():

    def __init__(self, twitterAPI, friendBizAPI):
        print ("Command Manager Instantiated")
        self._myCommands = [method for method in dir(botCommands) if callable(getattr(botCommands, method))]
        self.twitterAPI = twitterAPI
        self.friendBizAPI = friendBizAPI

    def dispatch(self, command, params, sender):
        if command in self._myCommands:
            getattr(self, command)(params, sender)
        else:
            print ("Unknown command: " + command)

    def echo(self, params, sender):
        reply = 'Hi @' + self.parseHandle(sender) + ', you said: ' + ' '.join(params)
        self.tweet(reply)

    def status(self, params, sender):
        handle = self.parseHandle(params[0])

        if userExists(handle, self.twitterAPI):
            u = self.friendBizAPI.getOrCreateUserByHandle(handle)
            self.tweet('@' + sender + ', ' + prettyStatus(u))

    def buy(self, params, sender):
        buyer  = self.parseHandle(sender)
        user_sold = self.parseHandle(params[0])

        if userExists(user_sold, self.twitterAPI):
            transaction = self.friendBizAPI.buy(buyer, user_sold)

            if transaction.status == TransactionValues.STATUS_SUCCESS:
                self.tweet('@' + sender + ', congrats! You bought @' + user_sold + ' for ' + str(transaction.amount))
            else:
                if transaction.reason == TransactionValues.BUY_FAIL_INSUFFICIENT_CREDIT:
                    b = self.friendBizAPI.getUserByHandle(buyer)
                    self.tweet('@' + sender + ', you don\'t have enough credit to buy @' +
                               user_sold +'. You have ' + str(b.balance) + ', you need ' + str(transaction.amount))

                elif transaction.reason == TransactionValues.BUY_FAIL_ALREADY_OWNER:
                    self.tweet('@' + sender + ', you already own @' + user_sold)

                elif transaction.reason == TransactionValues.BUY_FAIL_CANT_BUY_YOURSELF:
                    self.tweet('@' + sender + ', you can\'t buy yourself ;)')

                else:
                    print("Buy transaction failed: " + transaction.__repr__())

    def inventory(self, params, sender):
        u = self.friendBizAPI.getOrCreateUserByHandle(self.parseHandle(sender))


    def tweet(self, t):

        try:
            rateLimit(lambda: self.twitterAPI.update_status(t), self.twitterAPI)
            print ("Tweeted: " + t)

        except TweepError as e:
            print ("Tweet Failed. Error: " + e.__repr__())

    def parseHandle(self, handle):
        if handle[0] == '@': handle = handle[1:]
        return handle
