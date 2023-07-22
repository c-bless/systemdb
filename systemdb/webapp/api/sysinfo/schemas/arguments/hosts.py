from systemdb.core.regex import RE_SYSINFO_HOSTNAME
from systemdb.webapp.api.ma import ma
from marshmallow.validate import Regexp
from marshmallow import fields


class HostnameSearchSchema(ma.Schema):
    hostname = fields.String(required=True, validate=Regexp(regex=RE_SYSINFO_HOSTNAME))


class IPSearchSchema(ma.Schema):
    IP = fields.IP(required=True)

