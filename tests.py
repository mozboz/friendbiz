import unittest
import testCommandParsing
import friendBizApiTests

__author__ = 'james'

suite = unittest.TestLoader().loadTestsFromModule(friendBizApiTests)
unittest.TextTestRunner().run(suite)

suite = unittest.TestLoader().loadTestsFromModule(testCommandParsing)
unittest.TextTestRunner().run(suite)
