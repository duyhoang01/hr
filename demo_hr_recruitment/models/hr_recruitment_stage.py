# -*- coding: utf-8 -*-

from odoo import api, fields, models

class RecruitmentStage(models.Model):
    _inherit = "hr.recruitment.stage"

    is_send_plan = fields.Boolean('Cần gửi kế hoạch phỏng vấn')