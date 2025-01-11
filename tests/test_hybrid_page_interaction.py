import unittest
from selenium import webdriver
from config import settings
from pages.home_page import HomePage
from pages.hybrid_page import HybridPage
from pages.refine_page import RefinePage

class TestPageInteraction(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(settings.BASE_URL)
        

    def test_check_property_availability_and_return(self):
        # Navigate to the home page and perform a search
        home_page = HomePage(self.driver)
        home_page.search_location()
        home_page.select_dates()
        home_page.click_search_button()

        # Determine the current page and proceed accordingly
        current_url = self.driver.current_url
        if "/hybrid" in current_url:
            hybrid_page = HybridPage(self.driver, source_page="home")
            hybrid_page.check_property_availability()
            hybrid_page.return_to_previous_page()
            self.assertIn(settings.BASE_URL, self.driver.current_url, "Failed to return to the home page")
        elif "/refine" in current_url:
            refine_page = RefinePage(self.driver)
            refine_page.check_property_tiles()

            # After interacting with refine page, check if it navigates to hybrid page
            if "/hybrid" in self.driver.current_url:
                hybrid_page = HybridPage(self.driver, source_page="refine")
                hybrid_page.check_property_availability()
                hybrid_page.return_to_previous_page()
                self.assertIn("/refine", self.driver.current_url, "Failed to return to the refine page")
            
        
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()