from .base_page import BasePage
from selenium.webdriver.common.by import By
from .hybrid_page import HybridPage
from .refine_page import RefinePage
import time


class HomePage(BasePage):

    """
     Represents the Home Page of the application, providing methods to perform location search,
    date selection, and navigation handling for the Refine or Hybrid pages.
    """

    def search_location(self, location):
        """
         Perform a search using the specified location.

        Args:
            location (str): The location to be searched. The function types the location
                            character by character into the search box and selects one
                            from the suggestions.

        Raises:
            Exception: If no suggestions are found or an error occurs during the process.
        """
        search_box = self.wait_for_element(
            By.XPATH, "//input[@id='js-search-autocomplete']")
        search_box.clear()

        # Type location character by character
        for char in location:
            search_box.send_keys(char)
            time.sleep(0.3)

        time.sleep(2)  # Wait for suggestions to load

        try:
            # Wait for suggestions list
            suggestions_list = self.wait_for_element(
                By.XPATH,
                "//ul[@id='js-search-items']",
                timeout=10
            )

            # Get all suggestions
            suggestions = suggestions_list.find_elements(
                By.XPATH,
                ".//li[contains(@class, 'google-auto-suggestion-list')]"
            )

            time.sleep(1)

            if suggestions:
                # Select the first suggestion
                random_suggestion = suggestions[0]
                suggestion_text = random_suggestion.find_element(
                    By.CLASS_NAME, "suggested-place").text
                print(f"Selected location: {suggestion_text}")
                random_suggestion.click()
                time.sleep(1.5)
            else:
                raise Exception("No suggestions found")

        except Exception as e:
            print(f"Error selecting location: {str(e)}")
            raise

    def select_dates(self, check_in_date, check_out_date):
        """
       Select the specified check-in and check-out dates on the calendar.

        Args:
            check_in_date (str): The check-in date in 'YYYY-MM-DD' format.
            check_out_date (str): The check-out date in 'YYYY-MM-DD' format.

        Raises:
            Exception: If an error occurs during the date selection process.
        """
        try:
            print(
                f"Selecting dates - Check-in: {check_in_date}, Check-out: {check_out_date}")
            date_input = self.wait_for_element(
                By.XPATH, "//input[@id='js-date-range-display']")
            self.driver.execute_script("arguments[0].click();", date_input)
            time.sleep(1.5)

            # Select dates on the calendar
            check_in_day = int(check_in_date.split('-')[2])
            check_out_day = int(check_out_date.split('-')[2])

            check_in_xpath = f"//td[contains(@class, 'datepicker__month-day--valid') and text()='{
                check_in_day}']"
            check_out_xpath = f"//td[contains(@class, 'datepicker__month-day--valid') and text()='{
                check_out_day}']"

            check_in_element = self.wait_for_element(By.XPATH, check_in_xpath)
            self.driver.execute_script(
                "arguments[0].click();", check_in_element)
            time.sleep(1)

            check_out_element = self.wait_for_element(
                By.XPATH, check_out_xpath)
            self.driver.execute_script(
                "arguments[0].click();", check_out_element)
            time.sleep(1)

            continue_button = self.wait_for_element(
                By.XPATH, "//button[@id='js-date-select']", timeout=10)
            self.driver.execute_script(
                "arguments[0].click();", continue_button)
            time.sleep(1.5)

        except Exception as e:
            print(f"Error selecting dates: {str(e)}")
            raise

    def get_page_layout(self):
        """ Retrieve the layout type of the current page.

        Returns:
            str: The page layout type (e.g., "Refine" or "Hybrid").
            """
        try:
            page_layout = self.driver.execute_script(
                "return ScriptData.pageLayout;")
            print(f"Page Layout: {page_layout}")
            return page_layout
        except Exception as e:
            print(f"Error retrieving page layout: {str(e)}")
            return None

    def click_search_button(self):
        """
         Click the search button to execute the search action.

        Raises:
            Exception: If the search button cannot be clicked.
        """
        try:
            search_button = self.wait_for_element(
                By.XPATH, "//div[@id='js-btn-search']", timeout=20)
            self.driver.execute_script("arguments[0].click();", search_button)
            time.sleep(2)  # Wait for the search results to load
        except Exception as e:
            pass

    def handle_page_navigation(self, location, check_in_date, check_out_date):
        """
        Handle navigation to Refine or Hybrid pages after performing the search.

        Args:
            location (str): The selected location for the search.
            check_in_date (str): The check-in date in 'YYYY-MM-DD' format.
            check_out_date (str): The check-out date in 'YYYY-MM-DD' format.
        """
        page_layout = self.get_page_layout()
        if page_layout == "Refine":
            refine_page = RefinePage(
                self.driver, location, check_in_date, check_out_date)
            refine_page.check_property_tiles()
        elif page_layout == "Hybrid":
            hybrid_page = HybridPage(self.driver, source_page="home")
            hybrid_page.check_property_availability()
            hybrid_page.return_to_previous_page()

    def wait_for_any_element(self, locator_list, timeout=10):
        """
         Wait for any of the specified elements to be present on the page.

        Args:
            locator_list (list of tuples): A list of tuples where each tuple contains the locator strategy
                                           (e.g., By.XPATH) and the locator value (e.g., an XPath string).
            timeout (int): The maximum time to wait (in seconds) for the elements to appear.

        Returns:
            WebElement: The first visible element found in the locator list.

        Raises:
            Exception: If none of the elements in the locator list appear within the timeout period.
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
