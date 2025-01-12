
# Vacation Rental Automation

[![GitHub](https://img.shields.io/badge/GitHub-vacation_rental_automation-blue)](https://github.com/mdadnanshuvo/vacation_rental_automation)

Vacation Rental Automation is a Python-based test automation framework designed to automate the testing of vacation rental platforms. The framework is built using the Selenium WebDriver and follows the **Page Object Model (POM)** design pattern to ensure maintainability, scalability, and reusability.

---

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Page Workflow](#page-workflow)
- [DRY Principles Implemented](#dry-principles-implemented)
- [Setup Instructions](#setup-instructions)
- [How to Run Tests](#how-to-run-tests)
- [Contributing](#contributing)
- [License](#license)

---

## Features
- Automates testing of vacation rental web platforms.
- Selects random locations and date ranges for searches.
- Navigates through pages (e.g., Home, Refine, and Hybrid) using Selenium WebDriver.
- Checks property availability dynamically using pre-defined date ranges.
- Logs all test results in an Excel sheet for better traceability.
- Implements scrolling functionality for dynamically loaded pages.
- Follows the Page Object Model (POM) for better maintainability.

---

## Technologies Used
- **Python**: Core programming language.
- **Selenium**: Browser automation library.
- **Faker**: Data generation for random locations.
- **OpenPyXL**: Reading/writing Excel files.
- **Unittest**: Testing framework.
- **Git**: Version control.
- **VSCode**: Recommended development environment.

---

## Project Structure

vacation_rental_automation/
├── .vscode/                   # VSCode configuration files
├── config/                    # Configuration files
│   ├── __init__.py
│   ├── settings.py            # Application settings
├── data/                      # Data files (input/output)
│   ├── input.xlsx             # Input data file
│   ├── test_results.xlsx      # Test results log
├── env/                       # Virtual environment (not included in version control)
├── pages/                     # Page object classes
│   ├── __init__.py
│   ├── base_page.py           # Base class for page objects
│   ├── home_page.py           # Home page interactions
│   ├── hybrid_page.py         # Hybrid page interactions
│   ├── refine_page.py         # Refine page interactions
├── tests/                     # Test cases
│   ├── __init__.py
│   ├── test_automation.py     # Automation test cases
├── utils/                     # Utility functions and helpers
│   ├── __init__.py
│   ├── check_availability.py  # Availability check logic
│   ├── date_utils.py          # Utilities for date handling
│   ├── excel_utils.py         # Excel file handling utilities
│   ├── locations.py           # Location generation utilities
│   ├── num_of_tiles.py        # Logic to fetch the number of tiles
│   ├── scroll_utils.py        # Scrolling logic utilities
├── .gitignore                 # Git ignore file
├── main.py                    # Main application entry point
├── README.md                  # Project documentation
├── requirements.txt           # Python dependencies



---

## Page Workflow
The following is the high-level workflow of how the pages interact with each other in the automation:

1. **Home Page**:
   - Performs location search using random locations generated by `Faker`.
   - Selects random check-in and check-out dates using the `date_utils` module.
   - Clicks the search button to navigate to either the **Refine** or **Hybrid** page.

2. **Refine Page**:
   - Scrolls to load all property tiles using the utility function in `scroll_utils`.
   - Fetches the total number of property tiles using `num_of_tiles`.
   - Opens each property in a new tab to validate availability on the **Hybrid Page**.
   - Logs results, including location and date range, in an Excel file using `excel_utils`.

3. **Hybrid Page**:
   - Validates the availability of a property based on the selected date range.
   - Returns to the **Refine Page** after validation.

4. **Logging Results**:
   - All results, including location, date range, and availability status, are logged in `test_results.xlsx` in a professional and organized format.

---

## DRY Principles Implemented
The **Don't Repeat Yourself (DRY)** principle has been implemented throughout the project for maintainability and reusability. Here are some key examples:

1. **Utility Functions**:
   - Scrolling logic (`scroll_utils.py`), date generation (`date_utils.py`), and Excel handling (`excel_utils.py`) are modularized into reusable utilities.

2. **Base Page**:
   - Common methods for interacting with web elements (e.g., `wait_for_element`, `wait_for_any_element`) are centralized in `base_page.py` and inherited by all page classes.

3. **Property Availability Validation**:
   - A single method (`validate_property_availability`) in `check_availability.py` handles availability checks for all properties, reducing code duplication.

4. **Dynamic Test Parameters**:
   - Locations and date ranges are dynamically generated using `locations.py` and `date_utils.py`, eliminating hardcoded test inputs.

5. **Centralized Logging**:
   - Results are logged in a single, reusable function (`append_to_excel_file`) to ensure consistent output formatting across tests.

---

## Setup Instructions

### Prerequisites
1. Python 3.8 or higher installed on your system.
2. Google Chrome and the corresponding version of ChromeDriver installed.
3. Git installed for cloning the repository.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/mdadnanshuvo/vacation_rental_automation.git
   cd vacation_rental_automation
   ```

2. 
