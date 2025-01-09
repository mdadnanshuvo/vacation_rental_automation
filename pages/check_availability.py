# pages/check_availability.py

from .base_page import BasePage
from selenium.webdriver.common.by import By
import time

class PropertyPage(BasePage):
    def validate_property_availability(self):
        try:
            # Wait for any of the availability status elements without clicking any buttons
            availability_text = self.wait_for_any_element(
                [
                    (By.XPATH, "//div[@id='js-date-available']"),
                    (By.XPATH, "//div[@id='js-date-unavailable']")
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