{
    'name': 'Inventory Management',
    'version': '1.0.0',
    'category': 'Inventory',
    'summary': 'Custom Inventory Management System',
    'description': 'Module to manage inventory operations both administratively and operationally.',
    'author': 'Elhefnawy',
    'depends': ['base', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/product_view.xml',
        'views/inventory_oprations_view.xml',
        'views/category_view.xml',
        'views/move_product_history_view.xml',
        'views/location_view.xml',
        'reports/report_product_inv.xml',
        'reports/reorder_level_report.xml',


    ],
    'assets':{
        'web.report_assets_common': ['inventory_management/static/src/css/font.css']
    },
    'installable': True,
    'application': True,
}