# main.py

import unittest
from tests.test_hybrid_page_interaction import TestPageInteraction

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestPageInteraction))
    return test_suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())