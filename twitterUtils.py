from time import sleep
from sqlalchemy.exc import SQLAlchemyError

__author__ = 'james'

def userExists(username, twitterAPI):
    try:
        return twitterAPI.get_user(username)
    except SQLAlchemyError:
        return False


rateLimitWaitSeconds = 0

def rateLimit(twitterCall, twitterAPI):
    global rateLimitWaitSeconds
    if rateLimitWaitSeconds > 0:
        print "RATE LIMIT: Sleeping for " + rateLimitWaitSeconds + " seconds"
        sleep(rateLimitWaitSeconds)
        rateLimitWaitSeconds = 0

    twitterCall()

#    remaining = int(twitterAPI.last_response.getheader('x-rate-limit-remaining'))
#    limit = int(twitterAPI.last_response.getheader('x-rate-limit-limit'))
#    reset = int(twitterAPI.last_response.getheader('x-rate-limit-reset'))

    remaining = twitterAPI.rate_limit_status()

    print "(Twitter API) remaining: %s" % (remaining)


#
#a =    {u'rate_limit_context':
#                {u'access_token': u'4806590788-7FIv0Mo3TSKgeDxGc9koQU8LGPJCn4CT22C1BgD'},
#        u'resources': {u'help': {u'/help/tos': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                                 u'/help/settings': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                                 u'/help/privacy': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                                 u'/help/configuration': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                                 u'/help/languages': {u'reset': 1453171928, u'limit': 15, u'remaining': 15}},
#                       u'moments': {u'/moments/permissions': {u'reset': 1453171928, u'limit': 300, u'remaining': 300}},
#                       u'trends': {u'/trends/available': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                        u'/trends/closest': {u'reset': 1453171928, u'limit': 15, u'remaining': 15}, u'/trends/place':
#                    {u'reset': 1453171928, u'limit': 15, u'remaining': 15}},
#                       u'friendships': {u'/friendships/outgoing': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                        u'/friendships/show': {u'reset': 1453171928, u'limit': 180, u'remaining': 180},
#                        u'/friendships/incoming': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                        u'/friendships/no_retweets/ids': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                        u'/friendships/lookup': {u'reset': 1453171928, u'limit': 15, u'remaining': 15}},
#                       u'statuses': {u'/statuses/retweets_of_me': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                    u'/statuses/retweeters/ids': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                    u'/statuses/mentions_timeline': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                    u'/statuses/user_timeline': {u'reset': 1453171928, u'limit': 180, u'remaining': 180},
#                    u'/statuses/lookup': {u'reset': 1453171928, u'limit': 180, u'remaining': 180},
#                    u'/statuses/oembed': {u'reset': 1453171928, u'limit': 180, u'remaining': 180},
#                    u'/statuses/show/:id': {u'reset': 1453171928, u'limit': 180, u'remaining': 180},
#                    u'/statuses/friends': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                    u'/statuses/home_timeline': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                    u'/statuses/retweets/:id': {u'reset': 1453171928, u'limit': 60, u'remaining': 60}},
#                       u'feedback': {u'/feedback/show/:id': {u'reset': 1453171928, u'limit': 180, u'remaining': 180},
#                        u'/feedback/events': {u'reset': 1453171928, u'limit': 1000, u'remaining': 1000}},
#                       u'contacts': {u'/contacts/uploaded_by': {u'reset': 1453171928, u'limit': 300, u'remaining': 300},
#                                     u'/contacts/users_and_uploaded_by': {u'reset': 1453171928, u'limit': 300, u'remaining': 300},
#                                     u'/contacts/delete/status': {u'reset': 1453171928, u'limit': 300, u'remaining': 300},
#                                     u'/contacts/users': {u'reset': 1453171928, u'limit': 300, u'remaining': 300},
#                                     u'/contacts/addressbook': {u'reset': 1453171928, u'limit': 300, u'remaining': 300}},
#                       u'media': {u'/media/upload': {u'reset': 1453171928, u'limit': 500, u'remaining': 500}},
#                       u'business_experience': {u'/business_experience/keywords': {u'reset': 1453171928, u'limit': 450, u'remaining': 450}},
#                       u'geo': {u'/geo/similar_places': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                                u'/geo/id/:place_id': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                                u'/geo/reverse_geocode': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                                u'/geo/search': {u'reset': 1453171928, u'limit': 15, u'remaining': 15}},
#                       u'application': {u'/application/rate_limit_status': {u'reset': 1453171928, u'limit': 180, u'remaining': 179}},
#                       u'followers': {u'/followers/list': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                                      u'/followers/ids': {u'reset': 1453171928, u'limit': 15, u'remaining': 15}},
#                       u'collections': {u'/collections/list': {u'reset': 1453171928, u'limit': 1000, u'remaining': 1000},
#                                        u'/collections/show': {u'reset': 1453171928, u'limit': 1000, u'remaining': 1000},
#                                        u'/collections/entries': {u'reset': 1453171928, u'limit': 1000, u'remaining': 1000}},
#                       u'mutes': {u'/mutes/users/list': {u'reset': 1453171928, u'limit': 15, u'remaining': 15}, u'/mutes/users/ids':
#                               {u'reset': 1453171928, u'limit': 15, u'remaining': 15}}, u'saved_searches': {u'/saved_searches/show/:id':
#        {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#u'/saved_searches/list': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#u'/saved_searches/destroy/:id': {u'reset': 1453171928, u'limit': 15, u'remaining': 15}},
#                       u'blocks': {u'/blocks/list': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                                   u'/blocks/ids': {u'reset': 1453171928, u'limit': 15, u'remaining': 15}},
#                       u'users': {u'/users/suggestions/:slug': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                                  u'/users/lookup': {u'reset': 1453171928, u'limit': 180, u'remaining': 180},
#                                  u'/users/search': {u'reset': 1453171928, u'limit': 180, u'remaining': 180},
#                                  u'/users/suggestions/:slug/members': {u'reset': 1453171928, u'limit': 15, u'remaining': 15}
#                                  u'/users/derived_info': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                                  u'/users/show/:id': {u'reset': 1453171928, u'limit': 181, u'remaining': 181},
#                                  u'/users/suggestions': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                                  u'/users/report_spam': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                                  u'/users/profile_banner': {u'reset': 1453171928, u'limit': 180, u'remaining': 180}},
#                       u'search': {u'/search/tweets': {u'reset': 1453171928, u'limit': 180, u'remaining': 180}}, u'lists':
#                    {u'/lists/subscribers/show': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                     u'/lists/subscriptions': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                     u'/lists/statuses': {u'reset': 1453171928, u'limit': 180, u'remaining': 180},
#                     u'/lists/members/show': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                     u'/lists/subscribers': {u'reset': 1453171928, u'limit': 180, u'remaining': 180},
#                     u'/lists/list': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                     u'/lists/show': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                     u'/lists/memberships': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                     u'/lists/members': {u'reset': 1453171928, u'limit': 180, u'remaining': 180},
#                     u'/lists/ownerships': {u'reset': 1453171928, u'limit': 15, u'remaining': 15}},
#                       u'favorites': {u'/favorites/list': {u'reset': 1453171928, u'limit': 15, u'remaining': 15}},
#                       u'device': {u'/device/token': {u'reset': 1453171928, u'limit': 15, u'remaining': 15}},
#                       u'friends': {u'/friends/list': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                                    u'/friends/following/ids': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                                    u'/friends/ids': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                                    u'/friends/following/list': {u'reset': 1453171928, u'limit': 15, u'remaining': 15}},
#                       u'account': {u'/account/verify_credentials': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                                    u'/account/settings': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                                    u'/account/login_verification_enrollment': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                                    u'/account/update_profile': {u'reset': 1453171928, u'limit': 15, u'remaining': 15}},
#                       u'direct_messages': {u'/direct_messages/show': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                                            u'/direct_messages': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                                            u'/direct_messages/sent': {u'reset': 1453171928, u'limit': 15, u'remaining': 15},
#                                            u'/direct_messages/sent_and_received': {u'reset': 1453171928, u'limit': 15, u'remaining': 15}}}}
#
