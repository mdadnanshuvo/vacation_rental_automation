# tests/test_hybrid_page_interaction.py

import unittest
from selenium import webdriver
from config import settings
from pages.home_page import HomePage
from pages.hybrid_page import HybridPage

class TestHybridPageInteraction(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(settings.BASE_URL)
        self.driver.maximize_window()

    def test_check_property_availability_and_return(self):
        # Navigate to the home page and perform a search
        home_page = HomePage(self.driver)
        home_page.search_location()
        home_page.select_dates()
        home_page.click_search_button()

        # Check if the current page is the hybrid page
        if "/hybrid" in self.driver.current_url:
            hybrid_page = HybridPage(self.driver)
            hybrid_page.check_property_availability()
            hybrid_page.return_to_home_page()
            self.assertIn(settings.BASE_URL, self.driver.current_url, "Failed to return to the home page")
        else:
            self.fail("Did not navigate to the hybrid page")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()