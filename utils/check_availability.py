
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import time


class PropertyPage(BasePage):
    """
     Represents a Property Page, providing methods to validate property availability
     and handle interactions with availability status elements.
    """

    def validate_property_availability(self):
        """
         Validates the availability of a property for selected dates.

        This method checks for the presence of specific elements that indicate 
        whether the property is available or unavailable, without clicking any buttons.

        Returns:
            bool: True if the property is available, False otherwise.

        Raises:
            Exception: If an error occurs during validation.
        """

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
                return True  # Dates selected are available
            else:
                return False  # Dates selected are unavailable

        except Exception as e:
            print(f"Error validating property availability: {str(e)}")
            return False  # Handle exceptions by returning False

    def wait_for_any_element(self, locator_list, timeout=10):
        """ Waits for any one of the specified elements to be present and visible.

        Args:
            locator_list (list): A list of tuples, where each tuple contains a 
                                 locator strategy (e.g., By.XPATH) and a locator value.
            timeout (int): The maximum amount of time (in seconds) to wait for an element.

        Returns:
            WebElement: The first visible element found from the provided locators.

        Raises:
            Exception: If none of the specified elements are found within the timeout period.
            """
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
        raise Exception(f"None of the expected elements found within {
                        timeout} seconds")
