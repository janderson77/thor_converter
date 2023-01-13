from dataclasses import dataclass
from openpyxl import load_workbook
import datetime
from helpers import Employee, create_adjustment_import, create_generic_import, collect_sheet_names

test = load_workbook("maximus_test_file.xlsx", read_only=True)

@dataclass
class MaximusTC:
    name: str = None
    paycode: str = None
    line_item_id: str = None
    unit_pay: float = None
    unit_bill: float = None
    hours: float = None
    adjustment_pay: float = None
    adjustment_bill: float = None
    weekend_date: datetime = None

def get_weekend_date(date_string, paycode):
    # Refactor this code to only have the start be part of the conditional
    # After finding the start of the date string, the rest should be the same
    if paycode == "sick":
        starting = date_string.find("Pay") + 4
        counter = 0
        new_date_string = ""
        while counter <= 7:
            new_date_string = new_date_string + date_string[starting+counter]
            counter+=1
        
        new_date = datetime.datetime.strptime(new_date_string, '%m/%d/%y')
        # print(datetime.datetime.weekday(new_date))
        weekend_date = new_date + datetime.timedelta(days=6-datetime.datetime.weekday(new_date))
        return weekend_date

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

            employee.weekend_date = get_weekend_date(row[1], employee.paycode)

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
            employee.paycode = "covid-19"
            totalHours = None
            ending = row[1].lower().find(" hours")-1
            starting = row[1].find("(")+1
            if starting != ending:
                totalHours = [row[1][starting], row[1][ending]]
                totalHours = float("".join(totalHours))
            else:
                totalHours = float(row[1][starting])
            employee.hours = totalHours
            tcdata.append(employee)

        elif "bonus" in row[1].lower():
            employee.paycode = "bonus"
            employee.unit_pay = float(row[4])
            employee.unit_bill = float(row[3])
            tcdata.append(employee)

        else:
            # If none of the above, must be an adjustment.
            if "background" in row[1].lower():
                employee.paycode = "114"
                employee.adjustment_bill = float(row[3])
                tcdata.append(employee)
                continue
            elif "internet" in row[1].lower():
                employee.paycode = 151
            elif "monitor" in row[1].lower():
                employee.paycode = "27"
            else:
                employee.paycode = "ERROR"
            employee.adjustment_pay = float(row[4])
            employee.adjustment_bill = float(row[3])
            tcdata.append(employee)
    return tcdata
    

test_run = collect_maximux_data(test)
for i in test_run:
    print(i)