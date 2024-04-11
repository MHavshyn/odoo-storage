import base64
import datetime

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import os


class Storage(models.Model):
    _name = "file.storage"
    _description = "File Storage"
    _rec_name = 'name'

    name = fields.Char(string="Name", required=True)
    db_file = fields.Binary(string="File", attachment=True)
    status = fields.Selection([('Empty', 'Empty'), ('Filled', 'Filled')], string="Status", default='Empty', readonly=True)
    local_file_path = fields.Char(string="Local File Path")
    save_locally = fields.Boolean(string="Save locally", default=False)
    file_name = fields.Char('File Name')

    def _compute_local_file_path(self, file_name):
        # base_path = f'db_storage/files/{str(datetime.datetime.now())}/' # I don't know why it doesn't work, all permissions are set to 777
        # os.makedirs(base_path, exist_ok=True) # Permission denied
        # return os.path.join(base_path, file_name)
        return file_name

    def _save_file_locally(self, values):
        try:
            values['local_file_path'] = self._compute_local_file_path(values.get('file_name'))
            file_path = values['local_file_path']
            with open(file_path, 'wb+') as f:
                f.write(base64.b64decode(values['db_file']))
        except BaseException as e:
            raise ValidationError(_("Unable to save file."))

    def write(self, values):
        if 'db_file' in values and values['save_locally']:
            self._save_file_locally(values)
        values['status'] = 'Filled'
        return super(Storage, self).write(values)

    @api.model
    def create(self, values):
        if 'db_file' in values and values['save_locally']:
            self._save_file_locally(values)
        values['status'] = 'Filled'
        return super(Storage, self).create(values)

    def unlink(self):
        for record in self:
            if record.local_file_path:
                os.remove(record.local_file_path)
        return super(Storage, self).unlink()
