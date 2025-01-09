# pages/refine_page.py

from settings import BASE_URL
from .base_page import BasePage
from .check_availability import PropertyPage  # Import PropertyPage from check_availability.py
from selenium.webdriver.common.by import By
import time

class RefinePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.visit_count = 0

    def check_property_tiles(self, num_properties=20):
        try:
            # Find property tiles on the Refine page
            property_tiles = self.wait_for_elements(By.XPATH, "//div[contains(@class, 'title')]//a")
            num_checked = 0

            while num_checked < num_properties and self.visit_count < 2:
                for tile in property_tiles:
                    # Open the property in a new window
                    property_url = tile.get_attribute("href")
                    self.driver.execute_script("window.open(arguments[0]);", property_url)
                    self.driver.switch_to.window(self.driver.window_handles[-1])

                    # Check property availability
                    property_page = PropertyPage(self.driver)
                    property_page.validate_property_availability(self.visit_count)

                    # Close the property window and return to Refine page
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])

                    num_checked += 1
                    if num_checked >= num_properties:
                        break

                # Update visit count and return to Refine page if needed
                self.visit_count += 1
                if self.visit_count >= 2:
                    self.driver.get(BASE_URL)
                    print("Navigated back to the main page.")
                    break

        except Exception as e:
            print(f"Error checking property tiles on Refine page: {str(e)}")