from helpers import Employee
import pyexcel as p

def newTimecard(id, reg=0, ot=0):
    """Creates a new Employee dataclass instance and stores the employee id and either the regular or overtime hours associated with it in the first cell found with that employee id"""
    employee = Employee(id=id)
    employee.reg = reg
    employee.ot1 = ot
    return employee

def convertPBM():
    # List for the Employee data to be stored
    data = []
    tempID = 0

    # Opens the PBM provided spreadsheet
    xlsSheet = p.get_sheet(file_name="PBM.xls", start_row=10)

    # Iterates over the sheet
    for row in xlsSheet:
        temp_data = []
        if 'Grand Total:' in row or "Page" in row or "Page " in row:
            continue
        if len(row[0]) > 12:
            continue
        if "Regular Hours:" in row:
            tempID = int(row[0][4:])
            continue
        if "/" in row[0]:
            continue
        for index, value in enumerate(row):
            if row[index] != "":
                if type(value) == int:
                    temp_data.append(float(value))
                else:
                    temp_data.append(round(value,2))
        if len(temp_data) > 0:
            tc = newTimecard(tempID, temp_data[3], temp_data[4])
            data.append(tc)

    
    # for entry in data:
    #     print([entry.id, entry.reg, entry.ot1])

convertPBM()