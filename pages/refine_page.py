# pages/refine_page.py

from .base_page import BasePage
from .hybrid_page import HybridPage  # Import HybridPage
from selenium.webdriver.common.by import By
import time

class RefinePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def check_property_tiles(self, num_properties=20):
        try:
            # Increase the timeout for finding elements
            timeout = 45

            # Find property tiles on the Refine page
            print("Waiting for property tiles to load...")
            property_tiles = self.wait_for_elements(By.XPATH, "//div[contains(@class, 'property-tiles')]//div[contains(@class, 'title')]//a", timeout=timeout)
            num_checked = 0

            for tile in property_tiles:
                if num_checked >= num_properties:
                    break

                try:
                    # Open the property in a new window by clicking the title
                    href = tile.get_attribute("href")
                    print(f"Opening property: {href}")
                    self.driver.execute_script("window.open(arguments[0], '_blank');", href)
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    
                    # Wait for the Hybrid page to load
                    print("Waiting for the Hybrid page to load...")
                    self.wait_for_element(By.XPATH, "//div[@id='js-date-available'] | //div[@id='js-date-unavailable']", timeout=timeout)
                    time.sleep(5)  # Additional wait for the page to fully load

                    # Check property availability
                    hybrid_page = HybridPage(self.driver, source_page="refine")
                    hybrid_page.check_property_availability()

                    # Close the property window and return to Refine page
                    print("Closing property window and returning to Refine page...")
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])

                    num_checked += 1
                except Exception as e:
                    print(f"Error checking property tile: {str(e)}")
                    if len(self.driver.window_handles) > 1:
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[0])

        except Exception as e:
            print(f"Error checking property tiles on Refine page: {str(e)}")

    def wait_for_elements(self, by, value, timeout=10):
        """Wait for multiple elements to be present and visible."""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((by, value))
            )
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_all_elements_located((by, value))
            )
            return elements
        except Exception as e:
            print(f"Error waiting for elements: {str(e)}")
            raise