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

    department_id = fields.Many2one(required=True)
    user_id = fields.Many2one(domain=lambda self: self._get_user_id_domain())
    hr_responsible_id = fields.Many2one(domain=lambda self: self._get_hr_responsible_id_domain())
    approvers_id = fields.Many2one('res.users', string="Người duyệt yêu cầu", track_visibility='onchange',
           domain=lambda self: self._get_approvers_id_domain())
    need_director_to_participate = fields.Boolean('Cần Ban giám đốc tham dự!')

    def _get_user_id_domain(self):
        return ['|', ('groups_id', '=', self.env.ref('demo_hr_recruitment.hr_emloyee').id),
                ('groups_id', '=', self.env.ref('demo_hr_recruitment.manager_emloyee').id)]
    def _get_approvers_id_domain(self):
        return [('groups_id', '=', self.env.ref('demo_hr_recruitment.director_emloyee').id)]
    def _get_hr_responsible_id_domain(self):
        return [('groups_id', '=', self.env.ref('demo_hr_recruitment.hr_emloyee').id)]

    def send_mail_template(self, template, user_id):
        partner_ids = [user_id.partner_id.id]
        self.message_post_with_view(
            template,
            composition_mode='mass_mail',
            partner_ids=[(4, pid) for pid in partner_ids],
            auto_delete=True,
            auto_delete_message=True,
            parent_id=False,  # override accidental context defaults
            subtype_id=self.env.ref('mail.mt_note').id)
    @api.multi
    def action_request_approve(self):
        for rec in self:
            rec.send_mail_template('demo_hr_recruitment.message_user_required',rec.approvers_id)
        self.write({'state':'waiting_for_approval'})

    @api.multi
    def action_approve(self):
        for rec in self:
            rec.send_mail_template('demo_hr_recruitment.message_user_approve_required_for_hr_resp',rec.hr_responsible_id)
            if rec.user_id != rec.hr_responsible_id:
                rec.send_mail_template('demo_hr_recruitment.message_user_approve_required_for_recuit_resp', rec.user_id)
        self.write({'state': 'recruit'})

    @api.multi
    def action_cancel(self):
        for rec in self:
            partner_ids = [rec.user_id.partner_id.id]
            rec.send_mail_template('demo_hr_recruitment.message_user_refuse',rec.user_id)
        self.write({'state': 'cancel'})


