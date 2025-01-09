# pages/hybrid_page.py

from .base_page import BasePage
from .check_availability import PropertyPage  # Import PropertyPage from check_availability.py
from selenium.webdriver.common.by import By
from config.settings import BASE_URL
import time

class HybridPage(BasePage):
    def __init__(self, driver, source_page="home"):
        super().__init__(driver)
        self.source_page = source_page

    def check_property_availability(self):
        try:
            # Use PropertyPage class to validate property availability
            property_page = PropertyPage(self.driver)
            property_page.validate_property_availability()
        except Exception as e:
            print(f"Error checking property availability on hybrid page: {str(e)}")

    def return_to_previous_page(self):
        if self.source_page == "home":
            self.driver.get(BASE_URL)
            time.sleep(2)  # Wait for the homepage to load
            print("Navigated back to the home page.")
        elif self.source_page == "refine":
            self.driver.switch_to.window(self.driver.window_handles[0])
            print("Returned to the Refine page.")