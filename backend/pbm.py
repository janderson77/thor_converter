from helpers import Employee, create_pbm_import
import pyexcel as p

def newTimecard(id, reg=0, ot=0):
    """Creates a new Employee dataclass instance and stores the employee id and either the regular or overtime hours associated with it in the first cell found with that employee id"""
    employee = Employee(id=id)
    employee.reg = reg
    employee.ot1 = ot
    return employee

def convertPBM(export):
    # List for the Employee data to be stored
    data = []
    tempID = 0

    # Opens the PBM provided spreadsheet
    xlsSheet = p.get_sheet(file_type="xls", file_content=export, start_row=10)

    # Iterates over the sheet
    for row in xlsSheet:
        temp_data = []
        # Filters out rows with unusable data
        if 'Grand Total:' in row or "Page" in row or "Page " in row:
            continue
        # Filters out a specific row with unusable data the previous filter couldn't catch
        if len(row[0]) > 12:
            continue
        # Finds the row where the employee ID lives
        if "Regular Hours:" in row:
            # Extracts the employee ID from the number in this cell
            tempID = int(row[0][4:])
            continue
        # Skips over rows with dates in them by looking for a "/"
        if "/" in row[0]:
            continue
        # All other rows will either be blank, or have the employee's hours data.
        # A blank row will be iterated over, but no action taken.
        # A row with numerical data must be the employee's hours data, which is extracted.
        for index, value in enumerate(row):
            if row[index] != "":
                if type(value) == int:
                    temp_data.append(float(value))
                else:
                    temp_data.append(round(value,2))
        # If temp_data's length is greater than 0, that means all employee data has been found
        if len(temp_data) > 0:
            # Creates a new instance of the Employee dataclass, and inserts data into it
            tc = newTimecard(tempID, temp_data[3], temp_data[4])
            # Adds this Employee to the data list
            data.append(tc)

    return create_pbm_import(data)