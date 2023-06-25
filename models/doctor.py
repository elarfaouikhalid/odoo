from odoo import models,fields,api, _

class HospitalDoctor(models.Model):
    # _name = 'laivrison.order'
    _name = 'hospital.doctor'

    name = fields.Char(required=True)
    age = fields.Integer(required=True)
    gender = fields.Selection([
        ('male' , 'Male'),
        ('female' , 'Female'),
    ],required=True,default='male')

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('confirm', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True,default='draft')
    sequence = fields.Char(string="doctor Reference",required=True,index=True,default=lambda self: _('New'))

    patients = fields.One2many('hospital.patient','doctor')
    

    def confirm(self): 
        self.state = 'confirm'

    def done(self):
        self.state = 'done'

    def cancel(self):
        self.state = 'cancel'

    @api.model
    def create(self, vals):
        if vals.get('sequence', _('New')) == _('New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('hospital.doctor.sequence') or _('New')
        result = super(HospitalDoctor, self).create(vals)
        return result





    
