import os
from .base_page import BasePage
from .hybrid_page import HybridPage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchWindowException
import time
from urllib.parse import urlparse
from utils.scroll_utils import scroll_to_load_all_tiles  # Import the scroll utility
from utils.excel_utils import append_to_excel_file, ensure_data_folder_exists, create_excel_file, EXCEL_FILE_PATH
from utils.num_of_tiles import get_number_of_tiles  # Import the utility function


class RefinePage(BasePage):

    """
    Represents the Refine Page of the application, providing methods to check property tiles,
    log results, and handle interactions with Hybrid pages.

    """

    def __init__(self, driver, location, check_in_date, check_out_date):
        """
        Initialize the RefinePage with location and date range details.

        Args:
            driver (WebDriver): The WebDriver instance controlling the browser.
            location (str): The location selected for the search.
            check_in_date (str): The check-in date in 'YYYY-MM-DD' format.
            check_out_date (str): The check-out date in 'YYYY-MM-DD' format.

        """
        super().__init__(driver)
        self.location = location
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        ensure_data_folder_exists()
        if not os.path.exists(EXCEL_FILE_PATH):
            create_excel_file()

    def check_property_tiles(self):
        """
        Checks the availability of all property tiles on the Refine page and logs the results.

        This method scrolls through the page to load all tiles, processes each tile to open
        the associated Hybrid page, checks the availability of the property, and logs the results
        in an Excel file.

        Raises:
            Exception: If an error occurs during the property tile check process.
        """
        try:
            print("Fetching the total number of property tiles...")
            time.sleep(5)  # Allow time for the page to stabilize

            # Fetch the total number of tiles using the utility function
            try:
                total_tiles = get_number_of_tiles(self.driver)
                print(f"Total property tiles found: {total_tiles}")
            except Exception as e:
                print(f"Error fetching property tile count: {str(e)}")
                total_tiles = 10  # Fallback to default

            # Scroll to load all tiles
            print("Scrolling to load all property tiles...")
            # Use the utility function
            scroll_to_load_all_tiles(self.driver, delay=2)

            num_checked = 0
            checked_tiles = set()  # Track tiles already processed

            while num_checked < total_tiles:
                print(f"Waiting for property tiles to load... Checking tile {
                      num_checked + 1} of {total_tiles}.")
                time.sleep(5)  # Allow tiles to load

                # Fetch all currently visible tiles
                property_tiles = self.wait_for_elements(
                    By.XPATH, "//div[contains(@class, 'property-tiles')]//div[contains(@class, 'title')]//a", timeout=60
                )

                for tile in property_tiles:
                    if num_checked >= total_tiles:
                        break  # Stop if all tiles are processed

                    try:
                        href = tile.get_attribute("href")
                        title = tile.text

                        # Skip already processed tiles
                        if href in checked_tiles:
                            continue

                        if not href or not title:
                            print("Invalid tile data; skipping...")
                            continue

                        print(f"Opening property: {title} ({href})")
                        checked_tiles.add(href)  # Mark this tile as processed
                        time.sleep(5)  # Delay before opening the new tab
                        self.driver.execute_script(
                            "window.open(arguments[0], '_blank');", href)
                        self.driver.switch_to.window(
                            self.driver.window_handles[-1])

                        print("Waiting for the Hybrid page to load...")
                        # Delay to allow the Hybrid page to stabilize
                        time.sleep(5)
                        self.wait_for_element(
                            By.XPATH, "//div[@id='js-date-available'] | //div[@id='js-date-unavailable']", timeout=60)

                        hybrid_page = HybridPage(
                            self.driver, source_page="refine")
                        availability = hybrid_page.check_property_availability()
                        availability_status = 'Available' if availability else 'Unavailable'
                        print(f"Property availability for {
                              title}: {availability_status}")

                        # Log results in Excel
                        data = [
                            urlparse(href).netloc,  # Domain
                            href,  # URL
                            "Hybrid",  # Page
                            "Property available in date range",  # Test Case
                            availability,  # Passed
                            f"The property '{title}' is {
                                availability_status} in the specified date range."  # Comments
                        ]

                        additional_info = {
                            "location": self.location,
                            "check_in_date": self.check_in_date,
                            "check_out_date": self.check_out_date
                        }

                        append_to_excel_file(data, additional_info)

                        print(
                            "Closing property window and returning to Refine page...")
                        time.sleep(5)  # Delay for smooth transition back
                        self.driver.close()
                        self.driver.switch_to.window(
                            self.driver.window_handles[0])

                        num_checked += 1
                    except Exception as e:
                        print(f"Error processing property tile: {str(e)}")
                        print("Waiting before retrying...")
                        time.sleep(10)  # Wait before retrying
                        # Ensure focus returns to the Refine page
                        self.driver.switch_to.window(
                            self.driver.window_handles[0])

            print("Finished checking all property tiles.")
        except Exception as e:
            print(f"Error during property tile check: {str(e)}")
