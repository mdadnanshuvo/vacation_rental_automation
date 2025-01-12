# pages/hybrid_page.py

# Import PropertyPage from check_availability.py
from utils.check_availability import PropertyPage
from selenium.webdriver.common.by import By
from config.settings import BASE_URL
import time


class HybridPage(PropertyPage):  # Inherit from PropertyPage

    """
     Represents the Hybrid Page in the application, providing methods to check property availability
     and navigate back to the previous page.
    """

    def __init__(self, driver, source_page="None"):
        """
        Initialize the HybridPage.

        Args:
            driver (WebDriver): The WebDriver instance controlling the browser.
            source_page (str): The source page from which the Hybrid page was accessed.
                               Options: "home" or "refine". Defaults to "None".
         """

        super().__init__(driver)
        self.source_page = source_page

    def check_property_availability(self):
        """
        Validate the availability of the property on the Hybrid page.

        Returns:
            bool: True if the property is available within the specified date range, False otherwise.

        Raises:
            Exception: If an error occurs while checking property availability.
        """
        try:
            # Use the validate_property_availability method from PropertyPage
            return self.validate_property_availability()
        except Exception as e:
            print(f"Error checking property availability: {str(e)}")
            return False

    def return_to_previous_page(self):
        """
        Navigate back to the page from which the Hybrid page was accessed.

        If the source page is "home", it redirects to the homepage.
        If the source page is "refine", it switches back to the Refine page tab/window.
        """

        if self.source_page == "home":
            self.driver.get(BASE_URL)
            time.sleep(2)  # Wait for the homepage to load
            print("Navigated back to the home page.")
        elif self.source_page == "refine":
            self.driver.switch_to.window(self.driver.window_handles[0])
            print("Returned to the Refine page.")
