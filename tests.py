import unittest
import commandParsingTests
import friendBizApiTests

__author__ = 'james'

suite = unittest.TestLoader().loadTestsFromModule(friendBizApiTests)
unittest.TextTestRunner().run(suite)

suite = unittest.TestLoader().loadTestsFromModule(commandParsingTests)
unittest.TextTestRunner().run(suite)
