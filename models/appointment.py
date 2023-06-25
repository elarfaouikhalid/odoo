from odoo import models,fields,api, _
from datetime import date
# date time  is not date
# date time  get date and datetime 
#date get only date

class HospitalAppointment(models.Model):
    # _name = 'laivrison.order'
    _name = 'hospital.appointment'
    # _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    note = fields.Text(string='Description',required=True)
    appointment_date = fields.Date(required=True)
    sequence = fields.Char(string="appointment Reference",required=True,index=True,default=lambda self: _('New'))
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('confirm', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True,default='draft')
    

    @api.one
    @api.constrains('appointment_date')
    def check_date(self):
        # print(self.appointment_date)
        # print(self.patient)
        # print(self.patient.)
        # print('self ',self.env['hospital.patient'].search([('id','=', self.patient.id)]).name)
        # name_rec = self.env['hospital.appointment'].search([('patient','=', active_id)])
        name_rec = max(self.patient.appoinements.mapped('appointment_date'))
        print(self.patient.appoinements.mapped('appointment_date'))
        # print(name_rec.env['hospital.appointment'].browse(self._context.get('active_id')))
        if self.appointment_date < date.today():
            raise ValueError('the appointment date must by graet than today')
        # for rec in self.env['hospital.appointment'].search([]):
        if self.appointment_date < name_rec:
                raise ValueError('the appointment date must by graet than last appointments')


    @api.one
    def get_patient(self):
        print(self.env['hospital.patient'].search([('id','=', self.patient.id)], limit=1).name)
        # self.env['hospital.patient'].search([('id','=', self.patient.id)], limit=1).name
        print(self.patient.name)
    
    patient = fields.Many2one('hospital.patient',ondelete='cascade',readonly=True)
    # ,default=lambda self: self.patient.name)

    # def delete_record(self):
    #     record = self.env['hospital.appointment'].browse(self._context.get('active_id'))
    #     record.unlink()

    def confirm(self):
        print(self.patient.appoinements.ids)

    # def done(self):
    #     self.state = 'done'

    # def cancel(self):
    #     self.state = 'cancel'


    # @api.model
    # def create(self, vals):
    #     if vals.get('age') > 20 :
    #         return super(HospitalAppointment, self).create(vals)
    

    @api.model
    def create(self, vals):
        if vals.get('sequence', _('New')) == _('New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('hospital.appointment.sequence') or _('New')
        result = super(HospitalAppointment, self).create(vals)
        return result


    def send_mail(self):
        template_id = self.env.ref('hospital.patient_card_email_template').id
        self.env['mail.template'].browse(template_id).send_mail(self.id, force_send=True)
        # print(self.patient)  

        







    
