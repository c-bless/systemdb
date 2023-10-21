from flask import render_template, Response, url_for
from flask_login import login_required

from systemdb.webapp.sysinfo import sysinfo_bp
from systemdb.core.export.excel.hosts import generate_hosts_excel
from systemdb.core.export.excel.hosts import generate_hosts_excel_brief
from systemdb.core.export.excel.winlogon import generate_winlogon_excel
from systemdb.core.models.sysinfo import Host
from systemdb.core.reports import ReportInfo

####################################################################
# Hosts with DefaultPassword in Registry
####################################################################
@sysinfo_bp.route('/report/winlogon', methods=['GET'])
@login_required
def hosts_report_winlogon():
    hosts = Host.query.filter(Host.DefaultPassword != "").all()
    return render_template('sysinfo/reports/host_with_winlogon.html', hosts=hosts,
                           download_brief_url=url_for("sysinfo.hosts_report_winlogon_excel_brief"),
                           download_settings_url=url_for("sysinfo.hosts_report_winlogon_excel_settings"),
                           download_url=url_for("sysinfo.hosts_report_winlogon_excel_full"))


@sysinfo_bp.route('/report/winlogon/excel/full', methods=['GET'])
@login_required
def hosts_report_winlogon_excel_full():
    hosts = Host.query.filter(Host.DefaultPassword != "").all()
    output = generate_hosts_excel(hosts)
    return Response(output, mimetype="text/docx",
                    headers={"Content-disposition": "attachment; filename=hosts-with-winlogon-full.xlsx",
                             "Content-type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"})


@sysinfo_bp.route('/report/winlogon/excel/brief', methods=['GET'])
@login_required
def hosts_report_winlogon_excel_brief():
    hosts = Host.query.filter(Host.DefaultPassword != "").all()
    output = generate_hosts_excel_brief(hosts)
    return Response(output, mimetype="text/docx",
                    headers={"Content-disposition": "attachment; filename=hosts-with-winlogon-brief.xlsx",
                             "Content-type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"})

@sysinfo_bp.route('/report/winlogon/excel/settings', methods=['GET'])
@login_required
def hosts_report_winlogon_excel_settings():
    hosts = Host.query.filter(Host.DefaultPassword != "").all()
    output = generate_winlogon_excel(hosts)
    return Response(output, mimetype="text/docx",
                    headers={"Content-disposition": "attachment; filename=hosts-with-winlogon-brief.xlsx",
                             "Content-type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"})

class ReportPWInWinlogon(ReportInfo):

    def __init__(self):
        super().initWithParams(
            name="Password in Winlogon",
            category="Systemhardening",
            tags=["Cleartext password", "Missconfigured Autologon", "Winlogon", "Registry"],
            description='Report all hosts where a password is stored in clear text in Windows Registry',
            views=[("view", url_for("sysinfo.hosts_report_winlogon"))]
        )