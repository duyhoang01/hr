# -*- coding: utf-8 -*-

from odoo import api, fields, models

class Job(models.Model):
    _inherit = 'hr.job'

    state = fields.Selection(selection_add=[
      ('draft', 'Draft'),
      ('waiting_for_approval', 'Waiting for approval'),
    ])

