from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import query
from sqlalchemy.sql.expression import null
from models import User, TransactionLogItem, TransactionStatus

__author__ = 'james'


class friendBizAPI():

    def __init__(self, dbSessionMaker, config):
        print("friendBizAPI Instantiated")
        self.dbSessionMaker = dbSessionMaker
        # Permanent Session is used where there is not a long transaction, and making a new session
        # is not necessary
        self.permanentSession = self.dbSessionMaker()
        self.config = config

    def close(self):
        return False

    def getInventory(self, userId, session):
        u = session.query(User).filter(User.id == userId).one_or_none()
        return False if None else u.inventory


    def getOwnerID(self, userId, session):
        u = session.query(User.owner_id).filter(User.id == userId).one_or_none()
        return False if None else u.owner_id

    def buy(self, buyerHandle, userSoldHandle):

        # do everything here in one session
        buySession = self.dbSessionMaker()
        transactionLog = TransactionLog(self.dbSessionMaker)

        buyer = self.getOrCreateUserByHandle(buyerHandle, buySession)
        userSold = self.getOrCreateUserByHandle(userSoldHandle, buySession)
        buySession.commit()

        transactionLog.startLog(buyer, buyerHandle, userSold, userSoldHandle)

        if buyer.balance >= userSold.price:
            try:
                buyer.balance -= userSold.price

                if userSold.owner:
                    userSold.owner.balance += userSold.price

                userSold.owner = buyer
                userSold.price = self.priceStepAlgorithm(userSold)

                buySession.commit()
                transactionLog.success()

                return txStatus(status=txStatus.STATUS_OK)

            except SQLAlchemyError:
                buySession.rollback()

                transactionLog.fail(txStatus.DB_FAIL)

                return txStatus(status=txStatus.STATUS_FAIL, reason=txStatus.DB_FAIL)

        else:
            return txStatus(status=txStatus.STATUS_FAIL, reason=txStatus.BUY_FAIL_INSUFFICIENT_CREDIT)

    # this is the algorithm that generates a new price for a user who has just been bought
    def priceStepAlgorithm(self, user):
        return user.price * 2


    def getHistory(self, handle):
        return self.runInSession(lambda s: s.query(User).filter(User.handle == handle).one().transactions[:self.config['historyLength']])


    def getOrCreateUserByHandle(self, handle, session=None):
        def getOrCreateThisUser(s):
            u = s.query(User).filter(User.handle == handle).one_or_none()

            if u == None:
                u = self.createUser(handle, s)

            return u

        return self.runInSession(getOrCreateThisUser, session)

    # functionality for taking a function and a session and if the session is not set, making
    # one temporarily to run this function in
    def runInSession(self, func, session=None):
        s = self.permanentSession if session is None else session
        v = func(s)
        # if session is None: s.close()
        return v

    def createUser(self, handle, session=None):
        def createThisUser(s):
            u = User(
                handle=handle,
                balance=self.config['startingBalance'],
                price=self.config['startingPrice']
            )
            s.add(u)
            return u

        return self.runInSession(createThisUser, session)

    def getUserByID(self, id, session=None):
        return self.runInSession(
            lambda s: s.query(User).filter(User.id == id).one_or_none(),
            session)

    def getUserByHandle(self, handle, session=None):
        return self.runInSession(
            lambda s: s.query(User).filter(User.handle == handle).one_or_none(),
            session)


# make sure all critical information about transactions gets logged.
# transaction logging not working is a critical failure that must stop execution
class TransactionLog():
    def __init__(self, sessionMaker):
        self.sessionMaker = sessionMaker
        self.session = self.sessionMaker()
        self.transaction = TransactionLogItem()
        # self.session.add(self.transaction)

    def startLog(self, buyer, buyerHandle, userSold, userSoldHandle):
        self.transaction.description = "Buy: " + buyerHandle + " buying " + userSoldHandle
        self.transaction.buyer_id = buyer.id
        self.transaction.user_sold_id = userSold.id
        if userSold.owner_id:
            self.transaction.seller_id = userSold.owner_id
        self.transaction.status = TransactionStatus.STARTED
        self.transaction.amount = userSold.price
        self.session.add(self.transaction)
        self.session.commit()

    def success(self):
        try:
            self.transaction.status = TransactionStatus.SUCCESS
            self.session.commit()
            self.session.close()
        except SQLAlchemyError:
            print "Logging failed, exiting"
            exit(1)

    def fail(self, reason):
        try:
            self.transaction.status = TransactionStatus.FAIL
            self.transaction.reason = reason
            self.session.commit()
            self.session.close()
        except SQLAlchemyError:
            print "Logging failed, exiting"
            exit(1)




class txStatus():
    # Status
    STATUS_OK = 1
    STATUS_FAIL = 2

    # Reason
    BUY_FAIL_INSUFFICIENT_CREDIT = 1
    DB_FAIL = 2

    def __init__(self, status, reason=None):
        self.status = status
        self.reason = reason

