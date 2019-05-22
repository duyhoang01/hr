# -*- coding: utf-8 -*-

from odoo import api, fields, models

class RecruitmentRequest(models.Model):
    _name = "hr.request"
    _order = "date_needs"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']

    name = fields.Char('Title', required=True, translate=True)
    department_id = fields.Many2one('hr.department', 'Department', required=True)
    job_id = fields.Many2one('hr.job', 'Job Position')
    number_of_recruits  = fields.Integer('Number of recruits', required=True)
    number_of_recruited  = fields.Integer('Number of recruited')
    date_needs = fields.Datetime('Date needs new staff')
    request_by = fields.Many2one('res.users', 'Request by', readonly=True, default=lambda self: self.env.uid)
    type_id = fields.Many2one('hr.contract.type', string="Proposed Contract Type")

    reason = fields.Text(string='Reason', required=True)
    job_description = fields.Text(string='Job description', required=True)
    job_requirements = fields.Text(string='Job requirements', required=True)

    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id.id)
    application_ids = fields.One2many(related='job_id.application_ids')
    number_of_applicants = fields.Integer("Number of applicants", compute='_compute_number_of_applicants')

    @api.depends('application_ids')
    def _compute_number_of_applicants(self):
        for rec in self:
            rec.number_of_applicants = len(rec.application_ids)

    state = fields.Selection([
      ('draft', 'Draft'),
      ('waiting_for_approval', 'Waiting for approval'),
      ('approved', 'Approved'),
      ('process', 'Process'),
      ('done', 'Done'),
      ('cancel', 'Refused')], 'State', default='draft',
      copy=False, readonly=True, track_visibility='onchange')



    @api.multi
    def action_submit(self):
        self.write({'state': 'waiting_for_approval'})

    @api.multi
    def action_approve(self):
        self.write({'state': 'process'})

    @api.multi
    def action_refuse(self):
        self.write({'state': 'cancel'})

    @api.multi
    def action_set_to_draft(self):
        self.write({'state': 'draft'})

