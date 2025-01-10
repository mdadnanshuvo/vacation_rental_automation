# excel_utils.py

import openpyxl
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
import os

EXCEL_FILE_PATH = "data/test_results.xlsx"

def ensure_data_folder_exists():
    """Ensure the data folder exists."""
    os.makedirs(os.path.dirname(EXCEL_FILE_PATH), exist_ok=True)

def create_excel_file():
    """Create a new Excel file with the specified columns."""
    ensure_data_folder_exists()  # Ensure the data folder exists

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Test Results"

    columns = ["Key", "Url", "Page", "Test Case", "Passed", "Comments"]
    for col_num, column_title in enumerate(columns, 1):
        col_letter = get_column_letter(col_num)
        sheet[f'{col_letter}1'] = column_title

    workbook.save(EXCEL_FILE_PATH)
    print(f"Excel file '{EXCEL_FILE_PATH}' created successfully.")

def append_to_excel_file(data):
    """Append a new row of data to the existing Excel file."""
    if not os.path.exists(EXCEL_FILE_PATH):
        create_excel_file()  # Create the Excel file if it does not exist

    workbook = openpyxl.load_workbook(EXCEL_FILE_PATH)
    sheet = workbook.active

    sheet.append(data)
    workbook.save(EXCEL_FILE_PATH)
    print(f"Data appended to Excel file '{EXCEL_FILE_PATH}' successfully.")