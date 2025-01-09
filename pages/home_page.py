# pages/home_page.py

from .base_page import BasePage
from selenium.webdriver.common.by import By
from config.locations import get_random_location
from utils.date_utils import get_random_date_range
from .hybrid_page import HybridPage  # Import HybridPage
import random
import time

class HomePage(BasePage):
    def search_location(self):
        location = get_random_location()
        search_box = self.wait_for_element(By.XPATH, "//input[@id='js-search-autocomplete']")
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
                # Select random suggestion
                random_suggestion = random.choice(suggestions)
                suggestion_text = random_suggestion.find_element(By.CLASS_NAME, "suggested-place").text
                print(f"Selected location: {suggestion_text}")
                random_suggestion.click()
                time.sleep(1.5)
            else:
                raise Exception("No suggestions found")
                
        except Exception as e:
            print(f"Error selecting location: {str(e)}")

    def select_dates(self):
        try:
            check_in_date, check_out_date = get_random_date_range()
            print(f"Generated dates - Check-in: {check_in_date}, Check-out: {check_out_date}")
            
            # Wait for and click date input to open calendar
            date_input = self.wait_for_element(
                By.XPATH, 
                "//input[@id='js-date-range-display']",
                timeout=10
            )
            self.driver.execute_script("arguments[0].click();", date_input)
            time.sleep(1.5)  # Increased wait time for calendar to fully load
            
            # Get check-in date components
            check_in_day = int(check_in_date.split('-')[2])
            check_in_month = int(check_in_date.split('-')[1])
            check_in_year = int(check_in_date.split('-')[0])
            
            # Get check-out date components
            check_out_day = int(check_out_date.split('-')[2])
            check_out_month = int(check_out_date.split('-')[1])
            check_out_year = int(check_out_date.split('-')[0])
            
            # Select check-in date with more specific XPath
            check_in_xpath = (
                f"//td[contains(@class, 'datepicker__month-day--valid') and "
                f"not(contains(@class, 'datepicker__month-day--disabled')) and "
                f"normalize-space(text())='{check_in_day}'"
                f"]"
            )
            
            check_in_element = self.wait_for_element(By.XPATH, check_in_xpath)
            self.driver.execute_script("arguments[0].click();", check_in_element)
            time.sleep(1)
            
            # Select check-out date with more specific XPath
            check_out_xpath = (
                f"//td[contains(@class, 'datepicker__month-day--valid') and "
                f"not(contains(@class, 'datepicker__month-day--disabled')) and "
                f"normalize-space(text())='{check_out_day}'"
                f"]"
            )
            
            check_out_element = self.wait_for_element(By.XPATH, check_out_xpath)
            self.driver.execute_script("arguments[0].click();", check_out_element)
            time.sleep(1)
            
            # Click the continue button
            continue_button = self.wait_for_element(By.XPATH, "//button[@id='js-date-select']", timeout=10)
            self.driver.execute_script("arguments[0].click();", continue_button)
            time.sleep(1.5)
            
            # Check the page layout type
            page_layout = self.get_page_layout()
            if page_layout == "Hybrid":
                hybrid_page = HybridPage(self.driver)
                hybrid_page.check_property_availability()
                hybrid_page.return_to_home_page()
                self.filter_on_home_page()
                
        except Exception as e:
            print(f"Error selecting dates: {str(e)}")
            raise  # Re-raise the exception to handle it in the calling code

    def get_page_layout(self):
        """Retrieve the page layout type using Scriptdata.pageLayout."""
        try:
            page_layout = self.driver.execute_script("return ScriptData.pageLayout;")
            print(f"Page Layout: {page_layout}")
            return page_layout
        except Exception as e:
            print(f"Error retrieving page layout: {str(e)}")
            return None

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

    def click_search_button(self):
        search_button = self.wait_for_element(By.XPATH, "//div[@id='js-btn-search']")
        self.driver.execute_script("arguments[0].click();", search_button)
        time.sleep(2)  # Wait for the search results to load

    def filter_on_home_page(self):
        """Continue filtering on the home page after checking availability."""
        # Implement your filtering logic here
        pass