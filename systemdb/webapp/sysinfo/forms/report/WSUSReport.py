from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import Regexp, Optional

from systemdb.core.regex import RE_SYSINFO_SYSTEMGROUP
from systemdb.core.regex import RE_SYSINFO_LOCATION


class WSUSReportForm(FlaskForm):
    SystemGroup = StringField('SystemGroup', validators=[Regexp(regex=RE_SYSINFO_SYSTEMGROUP, message="Invalid input")] )
    Location = StringField('Location', validators=[Regexp(regex=RE_SYSINFO_LOCATION, message="Invalid input")] )

    InvertSystemGroup = BooleanField('Invert SystemGroup')
    InvertLocation = BooleanField('Invert Location')

    search = SubmitField('Search')

    brief = SubmitField('Excel Hosts (brief)')
    full = SubmitField('Excel Hosts (full)')
    wsus = SubmitField('Excel WSUS')