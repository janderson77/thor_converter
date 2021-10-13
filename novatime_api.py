from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment
from helpers import Employee, create_generic_import
import pyexcel as p
from io import BytesIO


def newTimecard(id, type, hours):
    """Creates a new Employee dataclass instance and stores the employee id and either the regular or overtime hours associated with it in the first cell found with that employee id"""
    emp = Employee(id=id)
    if type == 'reg':
        emp.reg = hours
    if type == 'ot1':
        emp.ot1 = hours
    return emp


def convertNT(export, client_name=None):
    """Iterates over a Novatime export file, converting the data into an Employee dataclass."""

    # List for the Employee data to be stored
    data = []

    # Opens the Novatime export and iterates over it
    xlsSheet = p.get_sheet(file_type="xls", file_content=export)
    for row in xlsSheet:
        # If there is already data in the data list
        if len(data) > 0:
            # if the employee id in the last index of the data list is the same as the current one
            if data[len(data)-1].id == row[0]:
                # if the current row is a regular time row
                if row[3].lower() == 'reg':
                    #                 # set the value of reg to the value in the current
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

    return create_generic_import(["Novatime", data], 1.165, client_name)
