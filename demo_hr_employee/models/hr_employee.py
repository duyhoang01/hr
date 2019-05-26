# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    timesheet_id = fields.Integer('Mã chấm công')

    @api.onchange('timesheet_id')
    def onchange_timesheet_id(self):
        if self.timesheet_id > 0:
            employee_id = self.env['hr.employee'].search([('timesheet_id', '=', self.timesheet_id)], limit=1)
            if employee_id:
                raise UserError(_("Mã Chấm công đã tồn tại!"))

