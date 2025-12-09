from odoo import models, fields, api


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    # Make partner_id not required so we can hide it
    partner_id = fields.Many2one('res.partner', required=False)


    contact_ids = fields.Many2many(
        'res.partner',
        'crm_lead_partner_rel',
        'lead_id',
        'partner_id',
        string='Contractant',
        domain=[('is_company', '=', True)]
    )
