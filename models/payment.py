from odoo import models,fields,api, _

class HospitalPayment(models.Model):
    # _name = 'laivrison.order'
    _name = 'hospital.payment'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)
    value = fields.Integer(required=True)
    
    sequence = fields.Char(string="patient Reference",required=True,index=True,default=lambda self: _('New'))
    
    patients = fields.One2many('hospital.patient','payment_terms')

    @api.model
    def create(self, vals):
        if vals.get('sequence', _('New')) == _('New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')
        result = super(HospitalPayment, self).create(vals)
        return result
    

   