# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'hospital',
    'version' : '1.1',
    'summary': 'hospital application',
    'sequence': -100,
    'description': """

    """,
    'category': 'project hospital',
    'website': 'https://www.odoo.com/page/billing',
    'depends' : ['base_setup', 'product', 'analytic', 'portal', 'digest','website'],
    'data': [
        'security/payment_security.xml',
        'security/ir.model.access.csv',
        'data/mail_template.xml',
        'data/sequence.xml',
        'data/sequence_doctor.xml',
        'data/sequence_appointment.xml',
        'data/cron.xml',
        'views/appointment.xml',
        'views/patient.xml',
        'views/doctor.xml',
        'views/payment.xml',
        'views/template.xml',
        'views/page.xml',
        'reports/reports.xml',
        'report/report_exel.xml',
    ],
    'installable' : True,
    'application' : True,
    'auto_install' : False,
    'license': 'LGPL-3',
}
