# Copyright 2023 Sodexis
# License OPL-1 (See LICENSE file for full copyright and licensing details).

{
    "name": "Purchase Dropshipping Slip",
    "summary": """This module is used the send the dropshipping delivery slip to the customer from the purchase order.""",
    "version": "15.0.1.0.0",
    "category": "Uncategorized",
    "website": "http://sodexis.com/",
    "author": "Sodexis",
    "license": "OPL-1",
    "installable": True,
    "application": False,
    "depends": [
        'purchase_stock',
        'sale_purchase',
    ],
    "data": [
        'report/purchase_dropshipping_reports.xml',
        'data/mail_template_data.xml',
        'report/purchase_dropshipping_templates.xml',
    ],
}
