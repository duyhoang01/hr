# -*- coding: utf-8 -*-

from odoo import api, fields, models

class Job(models.Model):
    _inherit = 'hr.job'

    state = fields.Selection([
      ('draft', 'Draft'),
      ('waiting_for_approval', 'Waiting for approval'),
      ('recruit', 'Recruitment in Progress'),
      ('open', 'Not Recruiting'),
      ('cancel', 'Cancel'),
    ], default='draft')

    @api.multi
    def action_request_approve(self):
        self.write({'state':'waiting_for_approval'})

    @api.multi
    def action_approve(self):
        self.write({'state': 'recruit'})

    @api.multi
    def action_cancel(self):
        self.write({'state': 'cancel'})

