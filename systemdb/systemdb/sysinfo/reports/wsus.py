from flask import render_template, Response, url_for

from .. import sysinfo_bp
from ..export_func import generate_hosts_excel, generate_hosts_excel_brief

from ...models.sysinfo import Host
from . import ReportInfo

####################################################################
# Hosts with WSUS over http
####################################################################
@sysinfo_bp.route('/hosts/report/wsus-http/excel/full', methods=['GET'])
def hosts_report_wsus_http_excel_full():
    hosts = Host.query.filter(Host.WUServer.like('http://%'))
    output = generate_hosts_excel(hosts)
    return Response(output, mimetype="text/xlsx",
                    headers={"Content-disposition": "attachment; filename=hosts-with-smbv1-full.xlsx",
                             "Content-type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" })


@sysinfo_bp.route('/hosts/report/wsus-http/excel/brief', methods=['GET'])
def hosts_report_wsus_http_excel_brief():
    hosts = Host.query.filter(Host.WUServer.like('http://%'))
    output = generate_hosts_excel_brief(hosts)
    return Response(output, mimetype="text/xlsx",
                    headers={"Content-disposition": "attachment; filename=hosts-with-smbv1-brief.xlsx",
                             "Content-type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" })


@sysinfo_bp.route('/hosts/report/wsus-http', methods=['GET'])
def hosts_report_wsus_http():
    hosts = Host.query.filter(Host.WUServer.like('http://%'))
    return render_template('host_list.html', hosts=hosts,
                           download_brief_url=url_for("sysinfo.hosts_report_wsus_http_excel_brief"),
                           download_url=url_for("sysinfo.hosts_report_wsus_http_excel_full"))




class ReportWSUSHttp(ReportInfo):

    def __init__(self):
        super().initWithParams(
            name="WSUS via http",
            category="Systemhardening",
            tags=["Systemhardening", "WSUS", "Cleartext protocol"],
            description='Report all hosts where the WSUS server is configured to be reached via http',
            views=[("view", url_for("sysinfo.hosts_report_wsus_http"))]
        )