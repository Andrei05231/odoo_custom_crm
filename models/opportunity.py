from odoo import models, fields, api


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    # Add many2many field for contacts
    contact_ids = fields.Many2many(
        'res.partner',
        'crm_lead_partner_rel',
        'lead_id',
        'partner_id',
        string='Contacts',
        domain=[('type', '=', 'contact')]
    )
    
    # Make partner_id not required so we can hide it
    partner_id = fields.Many2one('res.partner', required=False)


class CrmLeadPartner(models.Model):
    """Optional: Create a custom model if you need additional fields per contact"""
    _name = 'crm.lead.partner'
    _description = 'Lead Contact Association'
    
    lead_id = fields.Many2one('crm.lead', string='Lead', required=True, ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string='Contact', required=True, ondelete='cascade')
    name = fields.Char(related='partner_id.name', string='Name', readonly=True)
    email = fields.Char(related='partner_id.email', string='Email', readonly=True)
    phone = fields.Char(related='partner_id.phone', string='Phone', readonly=True)
    primary = fields.Boolean(string='Primary Contact', default=False)
    notes = fields.Text(string='Notes')