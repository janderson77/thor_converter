from openpyxl import load_workbook, Workbook
from openpyxl.styles import Alignment
from helpers import char_range, Employee, create_generic_import

# imports the Novatime export as well as the timecard import sheet
wb = load_workbook(filename="TWKPR.xlsx", read_only=True)
sheet = wb.active
center_aligned_text = Alignment(horizontal="center")

def newTimecard(id, type, hours):
        """Creates a new Employee dataclass instance and stores the employee id and either the regular or overtime hours associated with it in the first cell found with that employee id"""
        emp = Employee(id=id)
        if type == 'reg':
            emp.reg = hours
        if type == 'ot1':
            emp.ot1 = hours
        return emp

def convertPPNT():
    """Iterates over a Novatime export file, converting the data into an Employee dataclass."""
    # List for the Employee data to be stored
    data = []
    # Iterates over the Novatime export
    for row in sheet.iter_rows(min_row=1, max_row=sheet.max_row, values_only=True):
        # If there is already data in the data list
        if len(data) > 0:
            # if the employee id in the last index of the data list is the same as the current one
            if data[len(data)-1].id == row[0]:
                # if the current row is a regular time row
                if row[3].lower() == 'reg':
                    # set the value of reg to the value in the current iteration
                    data[len(data)-1].reg = row[4]
                else:
                    # Set the value of ot1 to the value in the current iteration
                    data[len(data)-1].ot1 = row[4]
            else:
                # Create a new time card for the current iteration's employee number
                tc = newTimecard(row[0], row[3].lower(), row[4])
                data.append(tc)
        else:
            # Create a new time card for the current iteration's employee number
            tc = newTimecard(row[0], row[3].lower(), row[4])
            data.append(tc)
    return data

# def create_pp_generic_import(data):
#     wb = Workbook()
#     new_sheet = wb.active

#     for i in char_range('A','G'):
#         new_sheet[f'{i}1'].alignment = center_aligned_text

#     new_sheet['A1'] = 'Employee Name'
#     new_sheet['B1'] = 'Emp #'
#     new_sheet['C1'] = 'Cust Name'
#     new_sheet['D1'] = 'Pay Rate'
#     new_sheet['E1'] = 'Reg Hrs'
#     new_sheet['F1'] = 'OT Hrs'
#     new_sheet['G1'] = 'DT Hrs'
#     # Sets the starting row to be edited as row 2
#     sheet_row = 2

#     # iterates over the data list
#     for e in data:
#         # sets column B to the value of employee id
#         new_sheet.cell(row=sheet_row, column=2).value = e.id

#         # Sets column C to the value of Papa Pita Bakery
#         new_sheet.cell(row=sheet_row, column=3).value = "Papa Pita Bakery"
        
#         # sets column E to the value of regular hours
#         new_sheet.cell(row=sheet_row, column=5).value = e.reg
        
#         # sets column F to the value of OT hours
#         new_sheet.cell(row=sheet_row, column=6).value = e.ot1
        
#         # Increments the sheet_row variable so that the next set of data is put on a new row
#         sheet_row+=1

#     # Saves as a new file
#     wb.save(filename="Papa Pita Novatime Import.xlsx")

import_data = convertPPNT()
create_generic_import(["Novatime",import_data], 1.165, "Papa Pita")