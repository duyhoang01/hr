# -*- coding: utf-8 -*-

from odoo import api, fields, models

class Applicant(models.Model):
    _inherit = "hr.applicant"

    # request_id = fields.Many2one('hr.request', 'Recruitment request')
    job_id = fields.Many2one(required=True)

    interview_start_time = fields.Datetime("Thời gian bắt đầus")
    interview_range_time = fields.Char('Thời lượng ước tính')
    interview_address = fields.Text('Địa điểm phỏng vấn')
    interview_note = fields.Text('Ghi chú')

    @api.model
    def create(self, vals):
        res = super(Applicant, self).create(vals)
        stage_ids = self.env['hr.recruitment.stage'].search([], limit=1, order="sequence asc").ids
        res.stage_id = stage_ids[0] if stage_ids else False
        return res

    @api.multi
    def write(self, vals):
        for rec in self:
            if 'stage_id' in vals and vals.get('stage_id'):
                stage_id = self.env['hr.recruitment.stage'].browse(vals.get('stage_id'))
                if stage_id and stage_id.is_send_plan:
                    rec.send_mail_invite_interview()
        res = super(Applicant, self).write(vals)

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

    def send_mail_invite_interview(self):
        dpm_id = self.job_id.department_id
        if dpm_id.manager_id:
            self.send_mail_template('demo_hr_recruitment.invite_manager', dpm_id.manager_id.user_id)
        if self.job_id.need_director_to_participate:
            self.send_mail_template('demo_hr_recruitment.invite_manager', self.job_id.approvers_id)