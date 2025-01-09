from .base_page import BasePage
from .home_page import HomePage
from .hybrid_page import HybridPage
from .refine_page import RefinePage  # Assuming you have a RefinePage class

class Workflow(BasePage):
    def run(self):
        home_page = HomePage(self.driver)
        home_page.search_location()
        home_page.select_dates()
        home_page.click_search_button()

        # Check the ScriptData.pageLayout to determine the page type
        script_data = self.driver.execute_script("return ScriptData;")
        page_layout = script_data.get("pageLayout", "")

        print(f"Page Layout: {page_layout}")

        if page_layout == "Hybrid":
            print("This is a Hybrid page.")
            hybrid_page = HybridPage(self.driver)
            hybrid_page.check_property_availability()
            hybrid_page.return_to_home_page()
            print("Returned to the home page.")
            
            # Verify if we are back to the home page
            if BASE_URL in self.driver.current_url:
                print("Successfully returned to the home page.")
            else:
                raise Exception("Failed to return to the home page.")

        elif page_layout == "Refine":
            print("This is a Refine page.")
            refine_page = RefinePage(self.driver)
            refine_page.perform_refinement_actions()
            print("Refinement actions completed.")

        else:
            print(f"Unexpected Page Layout: {page_layout}")

        print("Workflow run completed.")

if __name__ == "__main__":
    # Add code to initialize WebDriver and run the workflow
    from selenium import webdriver
    from config.settings import BASE_URL  # Assuming BASE_URL is defined in your settings

    driver = webdriver.Chrome()  # Replace with your WebDriver
    driver.get(BASE_URL)  # Use the base URL from settings
    driver.maximize_window()

    workflow = Workflow(driver)
    workflow.run()

    driver.quit()