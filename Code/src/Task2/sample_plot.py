import csv
from openpyxl import Workbook

def convert_csv_to_xlsx(file_loc, i):
    wb = Workbook()
    sheet = wb.active

    CSV_SEPARATOR = ";"

    with open(file_loc, 'r') as f:
        reader = csv.reader(f)
        for r, row in enumerate(reader):
            for c, col in enumerate(row):
                for idx, val in enumerate(col.split(CSV_SEPARATOR)):
                    cell = sheet.cell(row=r+1, column=idx+1)
                    cell.value = val

    wb.save("ACC_" + str(i) + ".xlsx")
    return '/home/ubuntu/Documents/Gesture_Recognition/ACC' + str(i) + '.xlsx'

for i in range(0,153):
    convert_csv_to_xlsx('/home/ubuntu/Documents/Gesture_Recognition/Gestures/Training/Right/ACC_' + str(i) + '.csv',i)
