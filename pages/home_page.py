# pages/home_page.py
from .base_page import BasePage
from selenium.webdriver.common.by import By
from config.locations import get_random_location
from utils.date_utils import get_random_date_range
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
            time.sleep(0.5)  # 300ms delay between each character
        
        time.sleep(5)  # Wait for final suggestions to load
        
        try:
            # Wait for suggestions list
            suggestions_list = self.wait_for_element(
                By.XPATH, 
                "//ul[@id='js-search-items']"
            )
            
            # Find all suggestion items
            suggestions = suggestions_list.find_elements(
                By.XPATH,
                ".//li[contains(@class, 'google-auto-suggestion-list')]"
            )
            
            time.sleep(5)  # Additional wait for suggestions to fully load
            
            # Filter out any empty/invalid suggestions
            valid_suggestions = [
                suggestion for suggestion in suggestions 
                if suggestion.get_attribute("data-place").strip()
            ]
            
            if valid_suggestions:
                # Select a random valid suggestion
                random_suggestion = random.choice(valid_suggestions)
                # Scroll the suggestion into view before clicking
                self.driver.execute_script("arguments[0].scrollIntoView(true);", random_suggestion)
                time.sleep(0.5)  # Brief pause after scrolling
                random_suggestion.click()
                time.sleep(2)  # Wait for selection to process
            else:
                raise Exception("No valid location suggestions found")
                
        except Exception as e:
            print(f"Error selecting location: {str(e)}")
            # Handle the error appropriately - maybe try again or use a default value

    def select_dates(self):
        check_in_date, check_out_date = get_random_date_range()
        
        # Open the date picker
        date_display = self.wait_for_element(By.XPATH, "//input[@id='js-date-range-display']")
        date_display.click()
        
        time.sleep(5)  # Wait for the calendar to appear
        
        # Select the check-in date
        check_in_day = int(check_in_date.split('-')[2])
        check_in_day_xpath = f"//td[contains(@class, 'datepicker__month-day--valid') and text()='{check_in_day}']"
        self.wait_for_element(By.XPATH, check_in_day_xpath).click()
        
        # Select the check-out date
        check_out_day = int(check_out_date.split('-')[2])
        check_out_day_xpath = f"//td[contains(@class, 'datepicker__month-day--valid') and text()='{check_out_day}']"
        self.wait_for_element(By.XPATH, check_out_day_xpath).click()
        
        # Click the continue button
        continue_button = self.wait_for_element(By.XPATH, "//button[@id='js-date-select']")
        continue_button.click()
        time.sleep(2)  # Wait for the date selection to be processed

    def click_search_button(self):
        search_button = self.wait_for_element(By.XPATH, "//div[@id='js-btn-search']")
        search_button.click()
        time.sleep(2)  # Wait for the search results to load