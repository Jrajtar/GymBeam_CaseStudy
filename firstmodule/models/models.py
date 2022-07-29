# -*- coding: utf-8 -*-

# from odoo import models, fields, api


from odoo import _, api, fields, models


class Employee(models.Model):
    _inherit = 'hr.employee'

    i_love_gb = fields.Boolean('i_love_gb')
    salary = fields.Integer(string="Salary", help="Translation for Salary")
    tax = fields.Integer(string="Tax", help="Translation for Tax")
    total_salary = fields.Integer(help="Translation for Total salary equal to salary + tax",
                                  compute='_compute_total_salary', string='Total salary')

    special_phone = fields.Char(
        help="Replaced  phone field by special_phone", string="Special Phone")

    employee_contacts = fields.Binary('employee_contacts')
    mail_to = fields.Char('mail_to')
    mail_subject = fields.Char('mail_subject')

    @api.depends('salary', 'tax')
    def _compute_total_salary(self):
        for rec in self:
            rec.total_salary = rec.salary + rec.tax

    @api.model_create_multi
    def create(self, vals):
        data = vals[0]
        if not data["special_phone"]:
            data["special_phone"] = "0901123456"
        res = super(Employee, self).create(vals)
        return res

    def write(self, vals):
        print("Origin----> ", self.special_phone)
        print("Values: ", vals)
        if not self.special_phone:
            vals['special_phone'] = "0901123456"
        return super(Employee, self).write(vals)

    def action_send(self):
        import xlrd
        import base64
        wb = xlrd.open_workbook(
        file_contents=base64.decodestring(self.employee_contacts))
        worksheet = wb.sheet_by_index(0)
        for row in range(worksheet.nrows):
            row_value = worksheet.row_values(row)
            self.fill_mail_subject(row_value[0],row_value[1])
    
    def fill_mail_subject(self, mail, subject):
        self.mail_to = mail
        self.mail_subject = subject
        template_id = self.env.ref("firstmodule.simple_email_template").id
        template = self.env["mail.template"].browse(template_id)
        template.send_mail(self.id, force_send=True)
        print("Mail sent!")