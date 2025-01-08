import unittest
from selenium import webdriver
from workflow import Workflow
from settings import BASE_URL

class TestWorkflow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()  # Replace with your WebDriver
        cls.driver.get(BASE_URL)  # Navigate to BASE_URL from settings
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_run_workflow(self):
        workflow = Workflow(self.driver)
        try:
            workflow.run()
            print("Workflow executed successfully.")
        except Exception as e:
            self.fail(f"Workflow execution failed: {e}")
