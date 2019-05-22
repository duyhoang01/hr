# -*- coding: utf-8 -*-

from odoo import api, fields, models

class Applicant(models.Model):
    _inherit = "hr.applicant"

    request_id = fields.Many2one('hr.request', 'Recruitment request')