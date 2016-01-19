from twitterUtils import userExists

__author__ = 'james'


# Process command tweeted to the bot
#
# Example command tweeted by someUser
#
#       !botName buy 10 fish
#
# For this command, dispatch will receive (command='buy', params=['10','fish'], sender='someUser')
# Note duplicate whitespace in original tweet intentionally lost

class botCommands():

    def __init__(self, twitterAPI, friendBizAPI):
        print ("Command Manager Instantiated")
        self._myCommands = [method for method in dir(botCommands) if callable(getattr(botCommands, method))]
        self.twitterAPI = twitterAPI
        self.friendBizAPI = friendBizAPI

    def dispatch(self, command, params, sender):
        if command in self._myCommands:
            getattr(self, command)(params, sender)

    def echo(self, params, sender):
        reply = 'Hi @' + sender + ', you said: ' + ' '.join(params)
        self.tweet(reply)

    def status(self, params, sender):
        handle = params[0]
        if (userExists(handle, self.twitterAPI)):
            u = self.friendBizAPI.getOrCreateUserByHandle(handle)
            self.tweet('@' + sender + ', ' + prettyStatus(u))

    def tweet(self, t):
        self.twitterAPI.update_status(t)
        print ("Tweeted: " + t)


def prettyStatus(u):
    status="@" + u.handle
    if u.owner:
        status += " is owned by @" + u.owner.handle
    else:
        status += " is not owned"

    status += ". Their price is %s, they have %s credits and own %s players" % (
        u.price, u.balance, len(u.inventory))

    return status
