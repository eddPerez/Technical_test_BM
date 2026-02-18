from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError
import json


class SaleOrderAPI(http.Controller):

    @http.route('/api/v1/sale-order', type='json', auth='none', methods=['POST'], csrf=False)
    def create_sale_order(self, **kwargs):
        """
        Endpoint REST para la creación de órdenes de venta.

        URL:
            POST /api/v1/sale-order

        Autenticación:
            Requiere Bearer Token en el header.
            El token corresponde a una API Key válida de Odoo (res.users.apikeys).

            Header requerido:
                Authorization: Bearer <API_KEY>

        Body (JSON):
            {
                "partner_id": int,
                "order_lines": [
                    {
                        "product_id": int,
                        "quantity": float,
                        "price_unit": float
                    }
                ]
            }

        Proceso:
            1. Valida la existencia y formato del Bearer Token.
            2. Verifica que la API Key sea válida.
            3. Cambia el entorno al usuario autenticado.
            4. Valida que el JSON recibido sea correcto.
            5. Verifica que el cliente exista.
            6. Verifica que los productos existan.
            7. Crea la orden de venta en estado draft (pending).
            8. Retorna el ID de la orden y el estado.

        Si la respuesta es exitosa:
            {
                "order_id": int,
                "status": "pending"
            }
        :param kwargs: Key Args (Body Json para procesar)
        :return: 
        """

        # Validación de token (Bearer Token) (API Key)
        auth_header = request.httprequest.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise UserError ("")

        token = auth_header.split(" ")[1]

        user = request.env['res.users.apikeys']._check_credentials(
            scope='rpc',
            key=token
        )

        if not user:
            raise ValidationError ("Error 'API Key' Incorrecta.")

        request.update_env(user=user)

        # OBTENER BODY JSON
        try:
            data = json.loads(request.httprequest.data)
        except Exception:
            raise ValidationError("JSON body Inválido")

        partner_id = data.get("partner_id")
        order_lines_data = data.get("order_lines", [])

        #  VALIDAR EXISTENCIA DE CLIENTE
        partner = request.env['res.partner'].browse(partner_id)
        if not partner.exists():
            return Response(
                json.dumps({"error": "Customer not found"}),
                status=404,
                content_type='application/json'
            )

        # VALIDAR EXISTENCIA DE PRODUCTOS
        if not order_lines_data:
            raise ValidationError("Sin datos de líneas de ventas")

        order_lines = []

        for line in order_lines_data:
            product = request.env['product.product'].browse(line.get("product_id"))

            if not product.exists():
                raise ValidationError("Producto no encontrado")

            order_lines.append((0, 0, {
                "product_id": product.id,
                "product_uom_qty": line.get("quantity", 1),
                "price_unit": line.get("price_unit", product.lst_price),
            }))

        sale_order = request.env['sale.order'].create({
            "partner_id": partner.id,
            "order_line": order_lines,
        })

        return {
            "order_id": sale_order.id,
            "status": "pending"
        }
