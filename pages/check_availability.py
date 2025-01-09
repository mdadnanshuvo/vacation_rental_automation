# pages/check_availability.py

import time
from .base_page import BasePage
from selenium.webdriver.common.by import By

class PropertyPage(BasePage):
    def validate_property_availability(self):
        try:
            check_availability_button = self.wait_for_element(By.XPATH, "//button[@id='js-btn-check-availability']", timeout=10)
            self.driver.execute_script("arguments[0].click();", check_availability_button)
            time.sleep(2)  # Wait for availability check
            
            availability_text = self.wait_for_any_element(
                [
                    (By.ID, "js-date-available"),
                    (By.ID, "js-date-unavailable")
                ],
                timeout=10
            )
            
            if availability_text.get_attribute("id") == "js-date-available":
                print("Dates selected are available")
            else:
                print("Dates selected are unavailable")
                
        except Exception as e:
            print(f"Error validating property availability: {str(e)}")
            raise

    def wait_for_any_element(self, locator_list, timeout=10):
        """Wait for any of the specified elements to be present."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            for by, locator in locator_list:
                try:
                    element = self.driver.find_element(by, locator)
                    if element.is_displayed():
                        return element
                except:
                    continue
            time.sleep(0.5)
        raise Exception(f"None of the expected elements found within {timeout} seconds")