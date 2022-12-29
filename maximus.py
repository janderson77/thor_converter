from dataclasses import dataclass
from openpyxl import load_workbook
from helpers import Employee, create_adjustment_import, create_generic_import, collect_sheet_names

test = load_workbook("maximus_test_file.xlsx", read_only=True)

@dataclass
class MaximusTC:
    name: str = None
    paycode: str = None
    line_item_id: str = None
    unit: float = None
    hours: float = None
    adjustment: float = None

def collect_maximux_data(sheet):
    ws = sheet[sheet.sheetnames[0]]
    tcdata = []

    for row in ws.iter_rows(min_row=ws.min_row, max_row=100, values_only=True):
        if row[0] == None:
            break
        if row[0].lower() == "id":
            continue

        employee = MaximusTC()

        employee_name_end_index = row[1].find(" -")
        employee.name = row[1][:employee_name_end_index]

        if "sick" in row[1].lower():
            employee.paycode = "sick"
            starting = row[1].find("(")
            sick_hours = ""
            for index, value in enumerate(row[1], start = starting+1):
                if row[1][index] == " ":
                    employee.hours = float(sick_hours)
                    break
                if row[1][index] != "(":
                    sick_hours = sick_hours + row[1][index]
            tcdata.append(employee)

        elif "covid" in row[1].lower():
            continue
        elif "bonus" in row[1].lower():
            continue
        else:
            continue
    return tcdata
    

test_run = collect_maximux_data(test)
print(test_run)