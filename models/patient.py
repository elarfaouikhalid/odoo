from odoo import models,fields,api, _
from datetime import datetime,timedelta
import re
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    # _name = 'laivrison.order'
    _name = 'hospital.patient'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)
    age = fields.Integer(required=True)
    gender = fields.Selection([
        ('male' , 'Male'),
        ('female' , 'Female'),
    ],required=True,default='male')
    image = fields.Binary("Image")
    sequence = fields.Char(string="patient Reference",required=True,index=True,default=lambda self: _('New'))
    operation_price = fields.Float()
    operation_name = fields.Char()
    operation_date = fields.Date()
    status_payment = fields.Char(String="Status",readonly=True,compute='status_amount')
    amount_due = fields.Float()
    end_date = fields.Date(readonly=True,compute='get_end_date')
    total = fields.Float(compute="calculate_total",store=True)
    email = fields.Char(required=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('paid', 'Paid'),
        ], string='Status',readonly=True, copy=False, index=True, track_visibility='onchange', track_sequence=3, default='draft')

    # @api.depends('operation_price')
    # def change_state(self):
    #     if self.total > 0 :
    #         self.filtered(lambda x: x.state == 'draft')\
    #         .write({'state': 'open'})
    #     if self.total == 0 and self.operation_price > 0 and self.operation_price == self.amount_due:
    #         self.env['hospital.patient'].filtered(lambda x: x.state == 'draft' or x.state == 'open')\
    #         .write({'state': 'paid'})

    # @api.onchange('amount_due')
    # def change_state(self):
    #     if self.total > 0 :
    #         self.filtered(lambda x: x.state == 'draft').write({'state': 'open'})
        # if self.total == 0 and self.operation_price > 0:
        #     self.filtered(lambda x: x.state == 'draft' or x.state == 'open')\
        #     .write({'state': 'paid'})

    
    def _get_default_currency_id(self):
        return self.env.user.company_id.currency_id.id


    currency_id = fields.Many2one("res.currency",string="Currency", readonly=True, required=True,default=_get_default_currency_id)
    
    def get_counter(self):
        count = self.env['hospital.appointment'].search_count([('id','in', self.appoinements.ids)])
        self.counter = count

    def get_open(self):
        counter = self.env['hospital.patient'].search_count([('status_payment','=', 'Open')])
        self.counter = counter
    
    # send mail to patient no paid
    def cron_patient(self):
        template_id = self.env.ref('hospital.patient_card_email_template').ids
        template = self.env['mail.template'].browse(template_id)
        patients = self.env['hospital.patient'].search([('total','>', 0)])
        for rec in patients:
            template.send_mail(rec.id, force_send=True)    
        print(template)

    doctor = fields.Many2one('hospital.doctor')
    appoinements = fields.One2many('hospital.appointment','patient')
    company_id = fields.Many2one('res.company')
    user_id = fields.Many2one('res.users')
    payment_terms = fields.Many2one('hospital.payment')
    counter = fields.Integer(compute='get_counter')
    open_state = fields.Integer(compute='get_open')

    def confirm(self):
        # print(self.appoinements.ids)
        print(self)

    # return list patient not paid
    @api.multi
    def patient_paid(self):
        return {
            'name': _('Patient paid'),
            'domain' : [('total','>',0)],
            'view_type': 'form',
            'res_model': 'hospital.patient',
            'view_id': False,
            'view_mode': 'tree,form' ,
            'type': 'ir.actions.act_window',
        }

    # return list appoinements of patient
    @api.multi
    def patient_appointment(self):
        return {
            'name': _('Appointments'),
            'domain' : [('id','in', self.appoinements.ids)],
            'view_type': 'form',
            'res_model': 'hospital.appointment',
            'view_id': False,
            'view_mode': 'tree,form' ,
            'type': 'ir.actions.act_window',
            'context': {'default_patient': self.id}
        }
    
    # @api.onchange('operation_price')
    # def calculate(self):
    #     self.amount_due = self.operation_price
    
    @api.depends('amount_due')
    def calculate_total(self):
        # if self.amount_due < self.operation_price:
        #     self.total = self.operation_price - self.amount_due
        # if self.amount_due == self.operation_price:
            self.total = self.operation_price - self.amount_due


    @api.one
    @api.depends('amount_due','total')
    def status_amount(self):
        if self.total > 0 and self.amount_due != 0:
            self.status_payment = 'Open'
            self.filtered(lambda x: x.state == 'draft')\
                .write({'state': 'open'})
        if self.total == 0 and self.operation_price > 0:
            self.status_payment = 'Paid'
            self.filtered(lambda x: x.state in ('draft', 'open'))\
            .write({'state': 'paid'})
        if self.amount_due == 0:
            self.status_payment = 'Draft'
    
    @api.one
    @api.depends('payment_terms.value')
    def get_end_date(self):
        # print(self.payment_terms.value)
        end_date = datetime.today().date() + timedelta(days=self.payment_terms.value)
        self.end_date = end_date
    
    # @api.one
    # @api.constrains('amount_due')
    # def check_amount(self):
    #     if self.amount_due > self.operation_price:
    #         raise ValueError('the amount due must be less than or equal operation_price')

    # @api.multi
    # @api.constrains('amount_due')
    # def check_state(self):
    #     if self.filtered(lambda x: x.state == 'paid') :
    #         raise ValueError('the operation of this patient already paid')
    def open(self):
        self.state = 'open'

    def paid(self):
        self.state = 'paid'

    # def cancel(self):
    #     self.state = 'cancel'


    # @api.model
    # def create(self, vals):
    #         return super(HospitalPatient, self).create(vals)
    

    @api.model
    def create(self, vals):
        if vals.get('sequence', _('New')) == _('New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')
        result = super(HospitalPatient, self).create(vals)
        return result


    def send_mail(self):
        template_id = self.env.ref('hospital.patient_card_email_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)   
        # print(self.env['hospital.patient'].browse(self._context.get('active_id')))  
        # print(self.patient) 
    
    @api.onchange('email')
    def validate_mail(self):
       if self.email:
        match = re.match\
            ('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',self.email)
        if match == None:
            raise ValidationError('Not a valid E-mail')

        







    
