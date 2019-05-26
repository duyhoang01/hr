# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    so_ngay_cong = fields.Float('Số ngày công', compute='compute_so_ngay_cong')
    so_ngay_cong_thuc_te = fields.Float('Số ngày công thực tế', compute='compute_so_ngay_cong_thuc_te')


    # tính số ngày thứ 7 và chủ nhật
    def get_number_of_sat_sun(self, date_from, date_to):
        date = date_from
        sat = 0
        sun = 0
        while date <= date_to:
            sat += 1 if date.weekday() == 5 else 0
            sun += 1 if date.weekday() == 6 else 0
            date = date + timedelta(days=1)
        return sat, sun

    # lấy danh sách ngày nghỉ lễ trong khoảng thời gian [date_form, date_to]
    def get_global_leaves(self, date_from, date_to):
        date_from = date_from.strftime(DATE_FORMAT)
        date_to = date_to.strftime(DATE_FORMAT)
        domain_1 = ['&', ('date_from', '>=', date_from), ('date_from', '<=', date_to)]
        domain_2 = ['&', ('date_from', '<=', date_from), ('date_to', '>=', date_to)]
        domain_3 = ['&', ('date_to', '>=', date_from), ('date_to', '<=', date_to)]
        global_leaves_1 = self.env['resource.calendar.leaves'].search(domain_1)
        global_leaves_2 = self.env['resource.calendar.leaves'].search(domain_2)
        global_leaves_3 = self.env['resource.calendar.leaves'].search(domain_3)
        global_leaves = global_leaves_1 | global_leaves_2 | global_leaves_3
        return global_leaves

    def check_day_in_global_leaves(self, date, global_leaves):
        for leave in global_leaves:
            date_from = datetime.strptime((leave.date_from.split(' '))[0], DATE_FORMAT)
            date_to = datetime.strptime((leave.date_to.split(' '))[0], DATE_FORMAT)
            if date_from <= date and date <= date_to: return True
        return False

    # Tính số ngày nghỉ lễ
    def get_number_of_days_in_global_leaves(self, date_from, date_to):
        global_leaves = self.get_global_leaves(date_from, date_to)
        date = date_from
        count = 0
        while date <= date_to:
            count += 1 if self.check_day_in_global_leaves(date, global_leaves) else 0
            date = date + timedelta(days=1)
        return count

    # tính số ngày trong khoảng thời gian [date_form, date_to]
    def get_days_in_range(self, date_from, date_to):
        date_delta = date_to - date_from
        return date_delta.days + 1

    @api.depends('date_from', 'date_to')
    def compute_so_ngay_cong(self):
        for rec in self:
            date_from = datetime.strptime(rec.date_from, DATE_FORMAT)
            date_to = datetime.strptime(rec.date_to, DATE_FORMAT)
            total = rec.get_days_in_range(date_from, date_to)
            sat, sun = rec.get_number_of_sat_sun(date_from, date_to)
            holiday = self.get_number_of_days_in_global_leaves(date_from, date_to)
            # print(holiday)
            rec.so_ngay_cong = total - sun - sat/2 - holiday

    def get_working_time(self, timesheet_ids):
        count = 0
        for rec in timesheet_ids:
            if rec.time_total >= 8:
                count +=1
            elif rec.time_total >=4:
                count += 0.5
        return count

    @api.depends('contract_id')
    def compute_so_ngay_cong_thuc_te(self):
        for rec in self:
            if rec.employee_id:
                if not rec.contract_id:
                    raise UserError(_("Phiếu lương chưa có Hợp đồng!"))
                employee = rec.contract_id.employee_id
                date_from = datetime.strptime(rec.date_from, DATE_FORMAT)
                date_to = datetime.strptime(rec.date_to, DATE_FORMAT)
                domain = [('employee_id', '=', employee.id),
                          ('date', '>=', date_from),
                          ('date', '<=', date_to)]
                timesheet_ids = rec.env['time.sheet'].search(domain)
                rec.so_ngay_cong_thuc_te = rec.get_working_time(timesheet_ids)

    @api.model
    def get_worked_day_lines(self, contracts, date_from, date_to):
        res = super(HrPayslip, self).get_worked_day_lines(contracts, date_from, date_to)
        for contract in contracts.filtered(lambda contract: contract.resource_calendar_id):
            attendances_SNC = {
                'name': _("Số ngày công"),
                'sequence': 1,
                'code': 'SNC',
                'number_of_days': self.so_ngay_cong,
                'number_of_hours': self.so_ngay_cong*8,
                'contract_id': contract.id,
            }
            attendances_SNTT = {
                'name': _("Số ngày công thực tế"),
                'sequence': 2,
                'code': 'NCTT',
                'number_of_days': self.so_ngay_cong_thuc_te,
                'number_of_hours': self.so_ngay_cong_thuc_te*8,
                'contract_id': contract.id,
            }
            res.append(attendances_SNC)
            res.append(attendances_SNTT)
        return res