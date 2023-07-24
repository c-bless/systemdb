from apiflask import Schema
from apiflask.fields import String
from apiflask.validators import Regexp

from systemdb.core.regex import RE_SYSINFO_REGISTRYCHECK_NAME


class RegistryCheckByNameSearchSchema(Schema):
    Name = String(validate=Regexp(regex=RE_SYSINFO_REGISTRYCHECK_NAME))
