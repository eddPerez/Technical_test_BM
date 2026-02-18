from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError
import json


class SaleOrderAPI(http.Controller):

    @http.route('/api/v1/sale-order', type='json', auth='none', methods=['POST'], csrf=False)
    def create_sale_order(self, **kwargs):
        """"""
        return False
