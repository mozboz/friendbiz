from sqlalchemy.exc import SQLAlchemyError

__author__ = 'james'

def userExists(username, twitterAPI):
    try:
        return twitterAPI.get_user(username)
    except SQLAlchemyError:
        return False