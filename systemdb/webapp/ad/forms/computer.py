from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import Regexp
from wtforms.validators import Optional
from wtforms.validators import IPAddress


from systemdb.core.regex import RE_AD_HOSTNAME
from systemdb.core.regex import RE_AD_OS
from systemdb.core.regex import RE_AD_DOMAINNAME
from systemdb.core.regex import RE_AD_SAMACCOUNT
from systemdb.core.regex import RE_AD_DISTINGUISHED_NAME
from systemdb.core.regex import RE_SID_USER_ACCOUNTS


class ADComputerSearchForm(FlaskForm):
    DNSHostName = StringField('DNSHostName', validators=[Regexp(regex=RE_AD_HOSTNAME, message="Invalid input")])
    SamAccountName = StringField('SamAccountName', validators=[Regexp(regex=RE_AD_SAMACCOUNT, message="Invalid input")])
    OperatingSystem = StringField('OperatingSystem', validators=[Regexp(regex=RE_AD_OS, message="Invalid input"), Optional()])
    SID = StringField('SID', validators=[Regexp(regex=RE_SID_USER_ACCOUNTS, message="Invalid input"), Optional()])

    IPv4Address = StringField('IPv4Address', validators=[IPAddress(), Optional()])
    IPv6Address = StringField('IPv6Address', validators=[IPAddress(), Optional()])

    Domain = StringField('Domain', validators=[Regexp(regex=RE_AD_DOMAINNAME, message="Invalid input")])
    DistinguishedName = StringField('DistinguishedName',
                                  validators=[
                                      Regexp(regex=RE_AD_DISTINGUISHED_NAME,message="Invalid input")]
                                  )

    Enabled = BooleanField('Enabled Account')
    Disabled = BooleanField('Disabled Account')

    GlobalCatalog_True = BooleanField('Globale Catalog (True)')
    GlobalCatalog_False = BooleanField('Globale Catalog (False)')


    InvertDNSHostName = BooleanField('Invert DNSHostName')
    InvertSID = BooleanField('Invert SID')
    InvertSamAccountName = BooleanField('Invert SamAccountName')
    InvertOperatingSystem = BooleanField('Invert OperatingSystem')
    InvertIPv4Address = BooleanField('Invert IPv4Address')
    InvertIPv6Address = BooleanField('Invert IPv6Address')
    InvertDomain = BooleanField('Invert Domain')
    InvertDistinguishedName = BooleanField('Invert DistinguishedName')

    search = SubmitField('Search')
    download = SubmitField('Download (Excel)')


class DCSearchForm(FlaskForm):
    Hostname = StringField('Hostname', validators=[Regexp(regex=RE_AD_SAMACCOUNT, message="Invalid input")])
    OperatingSystem = StringField('OperatingSystem', validators=[Regexp(regex=RE_AD_OS, message="Invalid input"), Optional()])

    IPv4Address = StringField('IPv4Address', validators=[IPAddress()])
    IPv6Address = StringField('IPv6Address', validators=[IPAddress()])

    Domain = StringField('Domain', validators=[Regexp(regex=RE_AD_DOMAINNAME, message="Invalid input")])
    DistinguishedName = StringField('DistinguishedName',
                                  validators=[
                                      Regexp(regex=RE_AD_DISTINGUISHED_NAME,message="Invalid input")]
                                  )

    Enabled = BooleanField('Enabled Account')
    Disabled = BooleanField('Disabled Account')

    GlobalCatalog_True = BooleanField('Globale Catalog (True)')
    GlobalCatalog_False = BooleanField('Globale Catalog (False)')


    InvertHostname = BooleanField('Invert Hostname')
    InvertOperatingSystem = BooleanField('Invert OperatingSystem')
    InvertIPv4Address = BooleanField('Invert IPv4Address')
    InvertIPv6Address = BooleanField('Invert IPv6Address')
    InvertDomain = BooleanField('Invert Domain')
    InvertDistinguishedName = BooleanField('Invert DistinguishedName')

    search = SubmitField('Search')
    download = SubmitField('Download (Excel)')


