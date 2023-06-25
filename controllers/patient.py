from odoo import http
from odoo.http import request


class PatientController(http.Controller):

    @http.route('/patient', auth='user',csrf=False)
    def account_invoice_onboarding(self):
        patients = request.env['hospital.patient'].sudo().search([])
        return request.render('hospital.homepage_patient',{
            'patients' : patients
        });
    
    @http.route('/patient/create', auth='user',csrf=False,method='POST')
    def account_invoice_create(self,**kw):
        patients = request.env['hospital.patient'].sudo().search([])
        vals = {
            'name' : kw['name'],
            'age' : kw['age'],
            'email' : kw['email'],
        }
        patients.create(vals)
    
    @http.route('/patient/delete/<int:id_patient>',auth="user", website=True,csrf=False)
    def account_invoice_delete(self,id_patient):
        patients = request.env['hospital.patient'].sudo().search([('id','=',id_patient)])
        patients.sudo().unlink()
        return request.redirect('/patient')
        
    
