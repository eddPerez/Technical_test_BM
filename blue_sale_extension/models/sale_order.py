# -*- coding: utf-8 -*-
from odoo import _
from odoo.models import Model
from odoo.fields import (Char, Selection, Boolean)
from odoo.exceptions import UserError


class SaleOrderInherit(Model):
    _inherit = "sale.order"

    def compute_can_edit_authorization_state(self):
        """
        Determina si el usuario actual puede editar el estado de autorización.

        Asigna True al campo `can_edit_authorization_state` si el usuario
        pertenece al grupo `blue_sale_extension.group_can_edit_authorization_state`,
        de lo contrario asigna False.

        :return: None
        """
        for rec in self:
            rec.can_edit_authorization_state = rec.env.user.has_group(
                'blue_sale_extension.group_can_edit_authorization_state')

    insurance_number = Char(
        string="Insurance Number"
    )
    authorization_status = Selection(
        selection=[
            ('draft', 'Draft'),
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        string="Authorization Status",
        default="draft",
        copy=False
    )
    can_edit_authorization_state = Boolean(
        string="Can Edit Authorization State",
        compute="compute_can_edit_authorization_state"
    )

    def action_confirm(self):
        """
        Herencia de método genérico de Odoo para agregar validación
        que restrinja la confirmación del pedido de venta si el estado
        de autorización no es 'Approved'.

        :return: super(). Funcionamiento genérico de 'action_confirm()'
        """
        res = super(SaleOrderInherit, self).action_confirm()

        if self.authorization_status != 'approved':
            raise UserError(_(
                'The order cannot be confirmed if the authorization has not been approved. '
                'Currently the state is %s'
            ) % self.authorization_status)

        return res
