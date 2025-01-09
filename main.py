import unittest
from tests.test_hybrid_page_interaction import TestPageInteraction

if __name__ == "__main__":
    loader = unittest.TestLoader()
    tests = loader.loadTestsFromTestCase(TestPageInteraction)
    runner = unittest.TextTestRunner()
    runner.run(tests)
