from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, query
from friendBizAPI import getInventory, getOwnerID
from helpers import getDbString
from models import User
from testData import setupUsers

__author__ = 'james'

import commands

engine = create_engine(getDbString(), pool_recycle=3600)
Session = sessionmaker(bind=engine)
s = Session()


def testCommandParsing(session):
    botname = 'friendbiz'
    command = 'test5'
    twitterData = {"created_at":"Thu Jan 14 21:31:18 +0000 2016","id":687748850279444480,"id_str":"687748850279444480","text":'@' + botname + ' ' + command,"source":"\u003ca href=\"http:\/\/twitter.com\" rel=\"nofollow\"\u003eTwitter Web Client\u003c\/a\u003e","truncated":False,"in_reply_to_status_id":'null',"in_reply_to_status_id_str":"null","in_reply_to_user_id":4806590788,"in_reply_to_user_id_str":"4806590788","in_reply_to_screen_name":"friendbiz","user":{"id":4806590788,"id_str":"4806590788","name":"zzo","screen_name":"friendbiz","location":'null',"url":'null',"description":'null',"protected":False,"verified":False,"followers_count":0,"friends_count":0,"listed_count":0,"favourites_count":0,"statuses_count":11,"created_at":"Thu Jan 14 18:26:16 +0000 2016","utc_offset":-28800,"time_zone":"Pacific Time (US & Canada)","geo_enabled":False,"lang":"en-gb","contributors_enabled":False,"is_translator":False,"profile_background_color":"F5F8FA","profile_background_image_url":"","profile_background_image_url_https":"","profile_background_tile":False,"profile_link_color":"2B7BB9","profile_sidebar_border_color":"C0DEED","profile_sidebar_fill_color":"DDEEF6","profile_text_color":"333333","profile_use_background_image":True,"profile_image_url":"http:\/\/abs.twimg.com\/sticky\/default_profile_images\/default_profile_6_normal.png","profile_image_url_https":"https:\/\/abs.twimg.com\/sticky\/default_profile_images\/default_profile_6_normal.png","default_profile":True,"default_profile_image":True,"following":'null',"follow_request_sent":'null',"notifications":'null'},"geo":'null',"coordinates":'null',"place":'null',"contributors":'null',"is_quote_status":False,"retweet_count":0,"favorite_count":0,"entities":{"hashtags":[],"urls":[],"user_mentions":[{"screen_name":"friendbiz","name":"zzo","id":4806590788,"id_str":"4806590788","indices":[0,10]}],"symbols":[]},"favorited":False,"retweeted":False,"filter_level":"low","lang":"en","timestamp_ms":"1452807078319"}

    config = {}
    config['botname'] = botname

    event = commands.event(twitterData, config)
    assert event.isCommand == True
    assert event.command == command

def testInventory(session):
    # setup data
    u1, u2, u3, t1 = setupUsers(session)

    # check inventory returns correct users
    # u1 should have two users in inventory: u2, u3
    inventory = getInventory(u1.id, session)
    assert len(inventory) == 2
    assert sorted([u.id for u in inventory]) == sorted([u3.id, u2.id])

def testOwner(session):
    u1, u2, u3, t1 = setupUsers(session)

    # u2 should be owned by u1
    assert getOwnerID(u2.id, session) == u1.id

testCommandParsing(s)
testInventory(s)
testOwner(s)


