# pages/hybrid_page.py

from .base_page import BasePage
from .check_availability import PropertyPage  # Import PropertyPage from check_availability.py
from selenium.webdriver.common.by import By
from config.settings import BASE_URL
import time

class HybridPage(BasePage):
    def check_property_availability(self):
        try:
            # Check for the availability status element
            availability_element = self.wait_for_element(By.XPATH, "//div[@class='availability-status']")
            print("Property availability checked on hybrid page.")
            
            # Use PropertyPage class to validate property availability
            property_page = PropertyPage(self.driver)
            property_page.validate_property_availability()
        except Exception as e:
            print(f"Error checking property availability on hybrid page: {str(e)}")
        
    def return_to_home_page(self):
        self.driver.get(BASE_URL)
        time.sleep(2)  # Wait for the homepage to load
        print("Navigated back to the home page.")