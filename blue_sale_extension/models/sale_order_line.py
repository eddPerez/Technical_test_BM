# -*- coding: utf-8 -*-
from odoo import _
from odoo.models import Model
from odoo.fields import (Char, Selection, Float)
from odoo.api import (depends, onchange)
from odoo.exceptions import UserError


class SaleOrderLineInherit(Model):
    _inherit = "sale.order.line"

    @depends('product_id', 'price_unit')
    def _compute_margin_line(self):
        """
        Calcula el margen total por línea de venta.

        El margen se obtiene de la diferencia entre el precio unitario de venta
        (`price_unit`) y el costo del producto (`product_id.standard_price`).

        :return: None. El resultado se asigna al campo computado `total_margin`.
        """
        for rec in self:
            rec.total_margin = (rec.price_unit - rec.product_id.standard_price)

    total_margin = Float(
        string="Total Margin",
        compute="_compute_margin_line",
        store=True
    )

    @onchange('total_margin')
    def _constrains_not_margin_negative(self):
        """
        Valida que el margen total no sea negativo.

        Lanza un error si el margen calculado es menor que cero,
        evitando que el precio de venta sea inferior al costo del producto.

        :raise UserError: Si el margen total es negativo.
        :return: None
        """
        for rec in self:
            if rec.total_margin < 0:
                raise UserError(
                    'The calculated margin is negative; please ensure '
                    'the selling price is not lower than the product price.'
                )
