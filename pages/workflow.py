from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from settings import BASE_URL

class Workflow:
    def __init__(self, driver):
        self.driver = driver
        self.home_page = HomePage(driver)
        self.search_results_page = SearchResultsPage(driver)

    def run(self):
        self.driver.get(BASE_URL)  # Navigate to the home page at the start
        self.driver.maximize_window()
        
        refine_page_visited = False
        properties_checked = 0
        max_properties_to_check = 20

        while properties_checked < max_properties_to_check:
            self.home_page.search_location()
            self.home_page.select_dates()

            if self.home_page.is_hybrid_page():
                print("Navigated to hybrid page.")
                self.home_page.return_to_home_page()
            elif self.home_page.is_refine_page():
                print("Navigated to refine page.")
                refine_page_visited = True
                properties_checked += self.search_results_page.validate_properties(properties_checked, max_properties_to_check)
            else:
                raise Exception("Unexpected navigation behavior.")

            if refine_page_visited and properties_checked >= max_properties_to_check:
                break

        print(f"Workflow completed. {properties_checked} properties validated.")
