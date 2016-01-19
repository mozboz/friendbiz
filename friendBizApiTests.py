import unittest
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, query
from commands import botCommands
from friendBizAPI import friendBizAPI
from helpers import getDbString
from models import User
from testData import setupUsers, id_generator, setupBuyUsers

__author__ = 'james'

class friendBizTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        engine = create_engine(getDbString(), pool_recycle=3600)
        cls.dbSessionMaker = sessionmaker(bind=engine)
        cls.friendBizAPI = friendBizAPI

    def setUp(self):
        self.session = self.dbSessionMaker()
        self.config = {"startingBalance":100, "startingPrice":1, "historyLength":10}
        self.friendBizAPI = friendBizAPI(self.dbSessionMaker, self.config)
        self.fakeTwitter = fakeTwitterAPI()
        self.command = botCommands(self.fakeTwitter, self.friendBizAPI)


    def tearDown(self):
        self.session.close()
        self.friendBizAPI.close()

class fakeTwitterAPI():

    def __init__(self):
        self.updateStatusCalls = []
        self.getUserCalls = []

    def update_status(self, message):
        self.updateStatusCalls.append(message)

    def get_user(self, username):
        self.getUserCalls.append(username)
        return True




class testFriendBizApi(friendBizTest):

    def testInventory(self):
        # setup data
        u1, u2, u3, t1 = setupUsers(self.session, self.config)

        # check inventory returns correct users
        # u1 should have two users in inventory: u2, u3
        inventory = self.friendBizAPI.getInventory(u1.id, self.session)
        assert len(inventory) == 2
        assert sorted([u.id for u in inventory]) == sorted([u3.id, u2.id])

    def testOwner(self):
        u1, u2, u3, t1 = setupUsers(self.session, self.config)

        # u2 should be owned by u1
        assert self.friendBizAPI.getOwnerID(u2.id, self.session) == u1.id

    def testGetOrCreate(self):

        handle = id_generator()
        u1 = self.friendBizAPI.getOrCreateUserByHandle(handle, self.session)
        self.session.commit()
        assert u1.id

        # repeating should get same ID
        u2 = self.friendBizAPI.getOrCreateUserByHandle(handle, self.session)
        assert u2.id == u1.id

    def testBuyWithExistingUsers(self):
        # u[0] owns u[1] and u[2]. u4 is not owned, does not own anything
        u = setupBuyUsers(self.session, self.config)
        # this is the price that u2 should be after it has been bought once
        targetPrice =  self.friendBizAPI.priceStepAlgorithm(u[1])

        self.friendBizAPI.buy(u[3].handle, u[1].handle)

        # make sure we don't accidentally test old data
        newSession = self.dbSessionMaker()
        new_u = [self.friendBizAPI.getUserByID(x.id, newSession) for x in u]
        self.session.close()

        assert new_u[1].owner_id == new_u[3].id
        assert new_u[3].balance == self.config['startingBalance'] - self.config['startingPrice']
        assert new_u[0].balance == self.config['startingBalance'] + self.config['startingPrice']
        assert new_u[1].price == targetPrice

    def testBuyWithNewUsers(self):
        uh = [id_generator(), id_generator()]
        for h in uh:
            assert self.session.query(User).filter(User.handle == h).one_or_none() is None

        self.friendBizAPI.buy(uh[0], uh[1])

        self.session.close()
        self.session = self.dbSessionMaker()

        # should now both exist
        u = [self.friendBizAPI.getUserByHandle(h) for h in uh]

        for i in u:
            assert i is not None

        assert u[0].balance == self.config['startingBalance'] - self.config['startingPrice']

    def testTransactions(self):
        u1, u2, u3, t1 = setupUsers(self.session, self.config)

        assert len(u1.transactions.all()) == 2
        assert u1.transactions[0].id == t1.id
        assert u2.transactions[0].id == t1.id

    def testHistory(self):
        u1, u2, u3, t1 = setupUsers(self.session, self.config)
        for x in range(0,20):
            self.friendBizAPI.buy(u1.handle, u3.handle)
            self.friendBizAPI.buy(u2.handle, u3.handle)

        assert len(self.friendBizAPI.getHistory(u1.handle)) == self.config['historyLength']


