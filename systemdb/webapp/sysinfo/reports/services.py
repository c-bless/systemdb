from flask import render_template, Response, url_for, request
from flask_login import login_required

from sqlalchemy import and_

from systemdb.webapp.sysinfo import sysinfo_bp
from systemdb.core.export.excel.services import generate_services_excel
from systemdb.core.export.excel.services import generate_services_acl_excel

from systemdb.core.models.sysinfo import Host
from systemdb.core.models.sysinfo import Service
from systemdb.core.models.sysinfo import ServiceACL
from systemdb.webapp.sysinfo.forms.report.ServiceReports import ServiceAclSearchForm
from systemdb.webapp.sysinfo.forms.services import ServiceUserContextSearchForm
from systemdb.core.querries.hardening import find_modifiable_services
from systemdb.core.querries.hardening import find_serviceACL_by_filter
from systemdb.core.querries.hardening import find_uqsp
from systemdb.webapp.sysinfo.forms.report.ServiceReports import UQSPReportForm
from systemdb.core.reports import ReportInfo
####################################################################
# Hosts with UQSP vulnerabilities
####################################################################
@sysinfo_bp.route('/report/services/uqsp/', methods=['GET', 'POST'])
@login_required
def hosts_report_services_uqsp():
    form = UQSPReportForm()

    host_filter = []

    if request.method == 'POST':

        if form.validate_on_submit():
            systemgroup = form.SystemGroup.data
            location = form.Location.data

            invertSystemgroup = form.InvertSystemGroup.data
            invertLocation = form.InvertLocation.data

            if len(systemgroup) > 0:
                if not invertSystemgroup:
                    host_filter.append(Host.SystemGroup.ilike("%" + systemgroup + "%"))
                else:
                    host_filter.append(Host.SystemGroup.notilike("%" + systemgroup + "%"))
            if len(location) > 0:
                if not invertLocation:
                    host_filter.append(Host.Location.ilike("%" + location + "%"))
                else:
                    host_filter.append(Host.Location.notilike("%" + location + "%"))

            services = find_uqsp(host_filter=host_filter)

            if 'excel' in request.form:
                output = generate_services_excel(services=services)
                return Response(output, mimetype="text/xlsx",
                                headers={"Content-disposition": "attachment; filename=uqsp.xlsx",
                                         "Content-type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"})

    else:
        services = []
    return render_template('sysinfo/reports/report_service_list.html', services=services, form=form,
                           report_name="Unquoted Service Pathes (UQSP)")



class ReportUQSP(ReportInfo):

    def __init__(self):
        super().initWithParams(
            name="UQSP",
            category="Systemhardening",
            tags=["Systemhardening", "Unqouted Service Pathes", "UQSP", "Service Misconfiguration"],
            description='Report all services where the path is not enclosed in quotes and which have a spaces in the path.',
            views=[("view", url_for("sysinfo.hosts_report_services_uqsp"))]
        )


####################################################################
# Services by ACL
####################################################################
@sysinfo_bp.route('/report/services/by-acl/', methods=['GET', 'POST'])
@login_required
def hosts_report_services_by_acl():
    form = ServiceAclSearchForm()
    host_filter = []
    service_filter = []
    if request.method == 'POST':
        if form.validate_on_submit():
            user = form.User.data
            invert_user = form.InvertUser.data
            permission = form.Permission.data
            invert_permission = form.InvertPermission.data

            systemgroup = form.SystemGroup.data
            location = form.Location.data

            invertSystemgroup = form.InvertSystemGroup.data
            invertLocation = form.InvertLocation.data

            if len(systemgroup) > 0:
                if not invertSystemgroup:
                    host_filter.append(Host.SystemGroup.ilike("%" + systemgroup + "%"))
                else:
                    host_filter.append(Host.SystemGroup.notilike("%" + systemgroup + "%"))
            if len(location) > 0:
                if not invertLocation:
                    host_filter.append(Host.Location.ilike("%" + location + "%"))
                else:
                    host_filter.append(Host.Location.notilike("%" + location + "%"))

            if len(user) > 0:
                if not invert_user:
                    service_filter.append(ServiceACL.AccountName.ilike("%" + user + "%"))
                else:
                    service_filter.append(ServiceACL.AccountName.notilike("%" + user + "%"))
            if len(permission) > 0:
                if not invert_permission:
                    service_filter.append(ServiceACL.AccessRight.ilike("%" + permission + "%"))
                else:
                    service_filter.append(ServiceACL.AccessRight.notilike("%" + permission + "%"))

            acls = find_serviceACL_by_filter(service_filter=service_filter, host_filter=host_filter)

            if 'excel' in request.form:
                output = generate_services_acl_excel(acls)
                return Response(output, mimetype="text/xslx",
                                headers={"Content-disposition": "attachment; filename=service_by_acl.xlsx",
                                         "Content-type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"})

            return render_template('sysinfo/reports/service_acl_search_list.html', form=form, acls=acls,
                               report_name="Service by ACL")
        else:
            print("Invalid input")
            return render_template('sysinfo/reports/service_acl_search_list.html', form=form,
                               report_name="Service by ACL")
    else:
        return render_template('sysinfo/reports/service_acl_search_list.html', form=form,
                               report_name="Service by ACL")


class ReportServiceByPermission(ReportInfo):

    def __init__(self):
        super().initWithParams(
            name="Service by ACL",
            category="Systemhardening",
            tags=["Systemhardening", "ACL", "User Permissions"],
            description='Report all services where the ACLs match specified User and Permission.',
            views=[("view", url_for("sysinfo.hosts_report_services_by_acl"))]
        )


####################################################################
# Services by user context
####################################################################
@sysinfo_bp.route('/report/services/by-usercontext/', methods=['GET', 'POST'])
@login_required
def hosts_report_services_by_usercontext():
    form = ServiceUserContextSearchForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            startname = form.Startname.data
            invert = form.Invert.data
            if not invert:
                services = Service.query.filter(Service.StartName.ilike("%" + startname + "%")).all()
            else:
                services = Service.query.filter(Service.StartName.notilike("%" + startname + "%")).all()

            if 'download' in request.form:
                output = generate_services_excel(services)
                return Response(output, mimetype="text/xslx",
                                headers={"Content-disposition": "attachment; filename=services_by_usercontext_{0}.xlsx".format(startname),
                                         "Content-type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"})
            else:
                return render_template('sysinfo/reports/service_startnamesearch_list.html',
                                       form=form,
                                       services=services)
        else:
            print("Invalid input")
            return render_template('sysinfo/reports/service_startnamesearch_list.html',
                                   form=form)
    else:
        return render_template('sysinfo/reports/service_startnamesearch_list.html',
                               form=form)

class ReportServiceByUsercontext(ReportInfo):

    def __init__(self):
        super().initWithParams(
            name="Service by user context (Startname)",
            category="Systemhardening",
            tags=["Systemhardening", "User Context", "User Permissions"],
            description='Report all services executed in context of specified user.',
            views=[("view", url_for("sysinfo.hosts_report_services_by_usercontext"))]
        )



####################################################################
# Services by ACL
####################################################################
@sysinfo_bp.route('/report/services/modifiable/', methods=['GET'])
@login_required
def hosts_report_modifiable_services():
    acls = find_modifiable_services()
    return render_template('sysinfo/reports/modifiable_services.html', acls=acls)


@sysinfo_bp.route('/report/services/modifiable/excel', methods=['GET'])
@login_required
def hosts_report_modifiable_services_excel():
    acls = find_modifiable_services()

    output = generate_services_acl_excel(acls=acls)
    return Response(output, mimetype="text/xlsx",
                    headers={"Content-disposition": "attachment; filename=modifiable-services.xlsx",
                             "Content-type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" })

class ReportModifiableServices(ReportInfo):

    def __init__(self):
        super().initWithParams(
            name="Modifiable services",
            category="Systemhardening",
            tags=["Systemhardening", "ACL", "User Permissions", "Modifiable Service"],
            description="Report all services where the ACLs allow modifications, excluding 'TrustedInstaller', "
                        "'System' and 'Administrator' account.",
            views=[("view", url_for("sysinfo.hosts_report_modifiable_services"))]
        )
