# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT

class TimeSheet(models.Model):
    _name = 'time.sheet'
    _rec_name = 'date'

    date = fields.Date('Ngày')
    weekdays = fields.Char('Thứ')
    employee_id = fields.Many2one('hr.employee','Nhân viên', required=True)
    department_id = fields.Many2one('hr.department', 'Phòng ban', required=True)
    position = fields.Char(related='employee_id.job_id.name',string='Chức vụ')
    checkin_1 = fields.Char('Thời gian vào 1')
    checkout_1 = fields.Char('Thời gian ra 1')
    checkin_2 = fields.Char('Thời gian vào 2')
    checkout_2 = fields.Char('Thời gian ra 2')
    time_total = fields.Float('Tổng số giờ', compute='compute_time_total')

    def convert_hour_minute_to_int(self, hour, minute):
        return hour + minute / 60

    def get_hour_minute_by_delta(self, delta):
        totsec = delta.total_seconds()
        hour = int(totsec // 3600)
        minute = int((totsec % 3600) // 60)
        return hour, minute
    def split_time_to_hour_minute(self, str_time):
        if str_time:
            times = str_time.split(':')
            hour = int(times[0]) if times[0] else 0
            minute = int(times[1]) if times[1] else 0
            return hour,minute
        return 0, 0

    def get_datetime(self, date, str_time):
        hour, minute = self.split_time_to_hour_minute(str_time)
        new_date = datetime(date.year, date.month, date.day, hour, minute, 0, 188394)
        return new_date

    def get_number_of_hour(self, start, end):
        date = datetime.strptime(self.date, DATE_FORMAT)
        date_start = self.get_datetime(date, start)
        date_end = self.get_datetime(date, end)
        delta = date_end - date_start
        hour,minute = self.get_hour_minute_by_delta(delta)
        return self.convert_hour_minute_to_int(hour, minute)

    @api.depends('checkin_1', 'checkin_2', 'checkout_1', 'checkout_2')
    def compute_time_total(self):
        for rec in self:
            if rec.checkin_1 and rec.checkout_1:
                rec.time_total += rec.get_number_of_hour(rec.checkin_1, rec.checkout_1)
            if rec.checkin_2 and rec.checkout_2:
                rec.time_total += rec.get_number_of_hour(rec.checkin_2, rec.checkout_2)

    @api.onchange('employee_id')
    def onchange_employee_id(self):
        self.department_id = self.employee_id.department_id

    @api.onchange('date')
    def onchange_date(self):
        weekdays = ''
        if date:
            w = date.weekday()
            if w == 0: weekdays = 'Hai'
            elif w == 1: weekdays = 'Ba'
            elif w == 2: weekdays = 'Tư'
            elif w == 3: weekdays = 'Năm'
            elif w == 4: weekdays = 'Sáu'
            elif w == 5: weekdays = 'Bảy'
            elif w == 6: weekdays = 'Chủ nhật'
            self.weekdays = weekdays