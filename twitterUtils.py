__author__ = 'james'

def userExists(username, twitterAPI):
    try:
        return twitterAPI.get_user(username)
    except:
        return False