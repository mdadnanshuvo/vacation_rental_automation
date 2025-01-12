import unittest
from selenium import webdriver
from config import settings
from pages.home_page import HomePage
from pages.hybrid_page import HybridPage
from pages.refine_page import RefinePage
from utils.locations import get_random_location
from utils.date_utils import get_random_date_range


class TestPageInteraction(unittest.TestCase):

    """
    Test suite for testing interactions between the Home, Refine, and Hybrid pages.

    This suite tests the ability to:
    - Perform a search using random locations and dates.
    - Handle navigation between Hybrid and Refine pages.
    - Check property availability and log results.
    """

    def setUp(self):
        """
         Set up the test environment.

        - Initializes a WebDriver instance using Chrome.
        - Navigates to the base URL defined in the settings module.
        """
        self.driver = webdriver.Chrome()
        self.driver.get(settings.BASE_URL)

    def test_check_property_availability_and_return(self):
        """
         Test the flow of checking property availability and returning to the appropriate page.

        Steps:
        1. Generate a random location and date range.
        2. Perform a search on the Home page.
        3. Navigate to either the Refine or Hybrid page based on the result.
        4. Check property availability on the Hybrid page or tiles on the Refine page.
        5. Return to the previous page and assert successful navigation.

        Raises:
            AssertionError: If the navigation back to the expected page fails.
        """

        # Generate location and random date range
        location = get_random_location()
        check_in_date, check_out_date = get_random_date_range()
        print(f"Test Location: {location}")
        print(
            f"Test Date Range: Check-in: {check_in_date}, Check-out: {check_out_date}")

        # Navigate to the home page and perform a search
        home_page = HomePage(self.driver)
        home_page.search_location(location)
        home_page.select_dates(check_in_date, check_out_date)
        home_page.click_search_button()

        current_url = None
        try:
            current_url = self.driver.current_url
        except Exception as e:
            print(f"Error retrieving current URL: {str(e)}")

        if "/hybrid" in current_url:
            hybrid_page = HybridPage(self.driver, source_page="home")
            hybrid_page.check_property_availability()
            hybrid_page.return_to_previous_page()
            self.assertIn(settings.BASE_URL, self.driver.current_url,
                          "Failed to return to the home page")
        elif "/refine" in current_url:
            refine_page = RefinePage(
                self.driver, location, check_in_date, check_out_date)
            refine_page.check_property_tiles()

    def tearDown(self):
        """
        Clean up the test environment.

        - Ensures the WebDriver instance is closed and terminated after the test.
        - Handles any exceptions that occur during teardown to avoid blocking further tests.
        """
        try:
            if self.driver.service.process:  # Check if the WebDriver process is active
                self.driver.quit()
                print("Browser session ended.")
        except Exception as e:
            print(f"Error during teardown: {str(e)}")


if __name__ == "__main__":
    unittest.main()


if __name__ == "__main__":
    unittest.main()
