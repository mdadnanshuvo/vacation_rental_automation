# tests/test_homepage_interaction.py

import unittest
from selenium import webdriver
from config import settings
from pages.home_page import HomePage

class TestHomepageInteraction(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(settings.BASE_URL)
        self.driver.maximize_window()

    def test_search_location_and_dates(self):
        home_page = HomePage(self.driver)
        home_page.search_location()  # No argument needed here
        home_page.select_dates()
        home_page.click_search_button()

        # Verify that the refine page or hybrid page is loaded
        self.assertTrue(
            "/refine" in self.driver.current_url or "/hybrid" in self.driver.current_url,
            "Neither refine nor hybrid page loaded"
        )

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()