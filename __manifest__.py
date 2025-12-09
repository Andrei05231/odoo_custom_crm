{
    "name": "Custom CRM Lead",
    "version": "0.1",
    "depends": ['base','crm'],
    "category": "Human Resources",
    "description": "custom fields in CRM lead",
    "data": [
        "views/lead_views.xml",
        'security/ir.model.access.csv'
    ],
    "installable": True,
    "auto_install": False,
}