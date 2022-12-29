from openpyxl import load_workbook
from helpers import Employee, create_adjustment_import, create_generic_import, collect_sheet_names

def collect_maximux_data(sheet):
    data = []
    return