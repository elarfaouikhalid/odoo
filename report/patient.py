from odoo import models

class PartnerXlsx(models.AbstractModel):
    _name = 'report.hospital.hospital_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, patients):
        sheet = workbook.add_worksheet('Report')
        bold = workbook.add_format({'bold': True})
        # print(patients.appoinements)
        rows = 0
        columns = 0
        sheet.write(rows, 0, 'Name', bold) 
        sheet.write(rows, 1, 'Age', bold) 
        sheet.write(rows, 2, 'appointment date', bold)
        sheet.write(rows+1, 0, patients.name, bold) 
        sheet.write(rows+1, 1, patients.age, bold) 
        for i, obj in enumerate(patients.appoinements):
            sheet.write(i+1, 2, obj.appointment_date, bold)
# sheet.write(rows, columns, parametre, format)