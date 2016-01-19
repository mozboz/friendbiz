from sqlalchemy.exc import SQLAlchemyError
from models import User, TransactionLogItem

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

    #
    def buy(self, buyerHandle, userSoldHandle):

        # do everything here in one session
        buySession = self.dbSessionMaker()
        transactionLog = TransactionLog(self.dbSessionMaker)

        buyer = self.getOrCreateUserByHandle(buyerHandle, buySession)
        userSold = self.getOrCreateUserByHandle(userSoldHandle, buySession)
        buySession.commit()

        transactionLog.startLog(buyer, buyerHandle, userSold, userSoldHandle)

        if buyerHandle == userSoldHandle:
            transactionLog.fail(TransactionValues.BUY_FAIL_CANT_BUY_YOURSELF)
            buySession.close()
            return transactionLog

        if userSold.owner == buyer:
            transactionLog.fail(TransactionValues.BUY_FAIL_ALREADY_OWNER)
            buySession.close()
            return transactionLog

        if buyer.balance >= userSold.price:
            try:
                buyer.balance -= userSold.price

                if userSold.owner:
                    userSold.owner.balance += userSold.price

                userSold.owner = buyer
                userSold.price = self.priceStepAlgorithm(userSold)

                buySession.commit()
                transactionLog.success()

                return transactionLog

            except SQLAlchemyError:
                buySession.close()

                transactionLog.fail(TransactionValues.DB_FAIL)

                return transactionLog

        else:
            transactionLog.fail(TransactionValues.BUY_FAIL_INSUFFICIENT_CREDIT)
            return transactionLog

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
        if session is None: s.commit()
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
class TransactionLog(TransactionLogItem):
    def __init__(self, sessionMaker):
        self.sessionMaker = sessionMaker
        self.session = self.sessionMaker(expire_on_commit=False)

    def __repr__(self):
        return super(TransactionLog, self).__repr__()

    def startLog(self, buyer, buyerHandle, userSold, userSoldHandle):
        self.description = "Buy: " + buyerHandle + " buying " + userSoldHandle
        self.buyer_id = buyer.id
        self.user_sold_id = userSold.id
        if userSold.owner_id:
            self.seller_id = userSold.owner_id
        self.status = TransactionValues.STATUS_STARTED
        self.amount = userSold.price
        self.session.add(self)
        self.session.commit()

    def success(self):
        try:
            self.status = TransactionValues.STATUS_SUCCESS
            self.session.commit()
            self.session.close()
        except SQLAlchemyError:
            print "Logging failed, exiting"
            exit(1)

    def fail(self, reason):
        try:
            self.status = TransactionValues.STATUS_FAIL
            self.reason = reason
            self.session.commit()
            self.session.close()
        except SQLAlchemyError:
            print "Logging failed, exiting"
            exit(1)

class TransactionValues():
    # Status
    STATUS_STARTED = "STARTED"
    STATUS_SUCCESS = "SUCCESS"
    STATUS_FAIL = "FAIL"

    # Reasons
    ## Buy
    BUY_FAIL_INSUFFICIENT_CREDIT = "BUY_FAIL_INSUFFICIENT_CREDIT"
    BUY_FAIL_CANT_BUY_YOURSELF = "BUY_FAIL_CANT_BUY_YOURSELF"
    BUY_FAIL_ALREADY_OWNER = "BUY_FAIL_ALREADY_OWNER"

    ## System
    DB_FAIL = "DB_FAIL"

