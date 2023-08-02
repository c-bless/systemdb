from io import BytesIO

import xlsxwriter


def generate_services_excel(services=[]):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {"in_memory": True})
    worksheet = workbook.add_worksheet()

    rows = []

    for s in services:
        tmp = [s.SystemName, s.Caption, s.Description, s.Name, s.StartMode, s.PathName, s.Started, s.StartName,
               s.DisplayName, s.Running, s.AcceptStop, s.AcceptPause, s.ProcessId, s.DelayedAutoStart,
               s.BinaryPermissionsStr, s.Host, s.Host.SystemGroup, s.Host.Location]
        rows.append(tmp)


    header_data = ["SystemName", "Caption", "Description", "Name", "StartMode", "PathName", "Started", "StartName",
               "DisplayName", "Running", "AcceptStop", "AcceptPause", "ProcessId", "DelayedAutoStart",
               "BinaryPermissionsStr", "Hostname", "SystemGroup", "Location"]

    header_format = workbook.add_format({'bold': True,
                                         'bottom': 2,
                                         'bg_color': '#CCCCCC'})

    for col_num, data in enumerate(header_data):
        worksheet.write(0, col_num, data, header_format)

    cell_format = workbook.add_format({'text_wrap': True})

    # Start from the first cell. Rows and columns are zero indexed.
    row = 1
    col = 0
    # Iterate over the data and write it out row by row.
    for service in rows:
        for c in service:
            if col == 14:
                worksheet.write(row, col, str(c), cell_format)
            else:
                worksheet.write(row, col, str(c))
            col += 1
        worksheet.autofilter("A1:O1")
        col = 0
        row += 1

    worksheet.autofit()
    # Close the workbook before streaming the data.
    workbook.close()

    # Rewind the buffer.
    output.seek(0)
    return output