import os
from .base_page import BasePage
from .hybrid_page import HybridPage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchWindowException, InvalidSessionIdException
import time
from urllib.parse import urlparse
from utils.excel_utils import append_to_excel_file, ensure_data_folder_exists, create_excel_file, EXCEL_FILE_PATH
from utils.num_of_tiles import get_number_of_tiles  # Import the utility function


class RefinePage(BasePage):
    def __init__(self, driver, location, check_in_date, check_out_date):
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
                total_tiles = 3  # Fallback to default

            num_checked = 0
            while num_checked < total_tiles:
                print(f"Waiting for property tiles to load... Checking tile {num_checked + 1} of {total_tiles}.")
                time.sleep(5)  # Allow tiles to load

                # Fetch all currently visible tiles
                property_tiles = self.wait_for_elements(
                    By.XPATH, "//div[contains(@class, 'property-tiles')]//div[contains(@class, 'title')]//a", timeout=60
                )

                # Iterate over visible tiles and test until total_tiles is reached
                for tile in property_tiles:
                    if num_checked >= total_tiles:
                        break  # Stop if we’ve already checked all tiles

                    try:
                        href = tile.get_attribute("href")
                        title = tile.text
                        if not href or not title:
                            print("Invalid tile data; skipping...")
                            continue

                        print(f"Opening property: {title} ({href})")
                        time.sleep(5)  # Delay before opening the new tab
                        self.driver.execute_script("window.open(arguments[0], '_blank');", href)
                        self.driver.switch_to.window(self.driver.window_handles[-1])

                        print("Waiting for the Hybrid page to load...")
                        time.sleep(5)  # Delay to allow the Hybrid page to stabilize
                        self.wait_for_element(By.XPATH, "//div[@id='js-date-available'] | //div[@id='js-date-unavailable']", timeout=60)

                        hybrid_page = HybridPage(self.driver, source_page="refine")
                        availability = hybrid_page.check_property_availability()
                        availability_status = 'Available' if availability else 'Unavailable'
                        print(f"Property availability for {title}: {availability_status}")

                        # Log results in Excel
                        data = [
                            urlparse(href).netloc,  # Domain
                            href,  # URL
                            "Hybrid",  # Page
                            "Property available in date range",  # Test Case
                            availability,  # Passed
                            f"The property '{title}' is {availability_status} in the specified date range."  # Comments
                        ]

                        additional_info = {
                            "location": self.location,
                            "check_in_date": self.check_in_date,
                            "check_out_date": self.check_out_date
                        }

                        append_to_excel_file(data, additional_info)

                        print("Closing property window and returning to Refine page...")
                        time.sleep(5)  # Delay for smooth transition back
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[0])

                        num_checked += 1
                    except NoSuchWindowException as e:
                        print(f"Window closed unexpectedly: {str(e)}")
                        if len(self.driver.window_handles) > 0:
                            self.driver.switch_to.window(self.driver.window_handles[0])
                    except Exception as e:
                        print(f"Error checking property tile: {str(e)}")
                        if len(self.driver.window_handles) > 1:
                            self.driver.close()
                            self.driver.switch_to.window(self.driver.window_handles[0])

            print("Finished checking all property tiles. Cleaning up...")
        except Exception as e:
            print(f"Error during property tile check: {str(e)}")
        finally:
            self.cleanup_and_quit()
