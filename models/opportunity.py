from odoo import models, fields, api


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    # Make partner_id not required so we can hide it
    partner_id = fields.Many2one('res.partner', required=False)

    contact_ids = fields.Many2many(
        'res.partner',
        'crm_lead_contact_rel',   
        'lead_id',
        'partner_id',
        string='Contractant',
        domain=[('is_company', '=', True)]
    )

    designer_ids = fields.Many2many(
        'res.partner',
        'crm_lead_designer_rel',  
        'lead_id',
        'partner_id',
        string='Proiectant General',
        domain=[('is_company', '=', False)]
    )

    sub_contractant_ids = fields.Many2many(
        'res.partner',
        'crm_lead_subcontractant_rel',  
        'lead_id',
        'partner_id',
        string='Subcontractanti',
    )

    # New field to display all contacts in a table
    all_contacts_display = fields.One2many(
        'crm.lead.contact.display',
        'lead_id',
        string='All Contacts',
        compute='_compute_all_contacts_display',
        store=True
    )

    def action_refresh_contacts_display(self):
        """Manual refresh trigger for contact display"""
        self._compute_all_contacts_display()
        return True

    @api.depends('contact_ids', 'designer_ids', 'sub_contractant_ids')
    def _compute_all_contacts_display(self):
        ContactDisplay = self.env['crm.lead.contact.display']
        
        for lead in self:
            # Clear existing computed records
            lead.all_contacts_display = [(5, 0, 0)]
            
            display_records = []
            
            # Add contacts from contact_ids
            for partner in lead.contact_ids:
                display_records.append((0, 0, {
                    'partner_id': partner.id,
                    'contact_type': 'contractant',
                    'name': partner.name,
                    'email': partner.email or '',
                    'phone': partner.phone or '',
                }))
            
            # Add contacts from designer_ids
            for partner in lead.designer_ids:
                display_records.append((0, 0, {
                    'partner_id': partner.id,
                    'contact_type': 'designer',
                    'name': partner.name,
                    'email': partner.email or '',
                    'phone': partner.phone or '',
                }))
            
            # Add contacts from sub_contractant_ids
            for partner in lead.sub_contractant_ids:
                display_records.append((0, 0, {
                    'partner_id': partner.id,
                    'contact_type': 'subcontractant',
                    'name': partner.name,
                    'email': partner.email or '',
                    'phone': partner.phone or '',
                }))
            
            lead.all_contacts_display = display_records


class CrmLeadContactDisplay(models.TransientModel):
    _name = 'crm.lead.contact.display'
    _description = 'CRM Lead Contact Display (for computed table)'

    lead_id = fields.Many2one('crm.lead', string='Lead', required=True, ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string='Partner', readonly=True)
    contact_type = fields.Selection([
        ('contractant', 'Contractant'),
        ('designer', 'Proiectant General'),
        ('subcontractant', 'Subcontractant'),
    ], string='Type', readonly=True)
    name = fields.Char(string='Name', readonly=True)
    email = fields.Char(string='Email', readonly=True)
    phone = fields.Char(string='Phone', readonly=True)