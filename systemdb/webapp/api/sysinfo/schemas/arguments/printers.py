from marshmallow.validate import Regexp
from flask_marshmallow.fields import fields

from systemdb.core.regex import SYSINFO_PRINTERNAME
from systemdb.webapp.api.ma import ma


class PrinterMatchSearchSchema(ma.Schema):
    names = fields.List(fields.String(validate=Regexp(regex=SYSINFO_PRINTERNAME)))
