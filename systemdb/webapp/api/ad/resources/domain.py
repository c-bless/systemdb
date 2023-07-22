from http import HTTPStatus
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy import and_

from systemdb.core.models.activedirectory import ADDomain, ADUser, ADGroup, ADComputer, ADDomainController, \
    ADPasswordPolicy
from systemdb.webapp.api.ad.schemas.responses.domain import ADDomainSchema, ADUserSchema, ADGroupSchema, \
    ADComputerSchema, ADGroupWithMembersSchema
from systemdb.webapp.api.ad.schemas.responses.domain import ADDomainControllerSchema, ADPasswordPolicySchema
from systemdb.webapp.api.ad.schemas.arguments.groups import GroupNameSearchSchema

blp = Blueprint('ActiveDirectory - Domain', 'ad_domain_api' , url_prefix='/api/ad',
             description="Review active directory data collected by domain-collector PowerShell scripts.")


@blp.route("/domain/<int:domain_id>/groups/domainadmins/")
class DomainDomainAdminGroupView(MethodView):

    @blp.doc(description="Returns the domain admin group for the specified domain.",
             summary="Find the domain admin group for the specified domain."
             )
    @blp.response(HTTPStatus.OK.value, ADGroupWithMembersSchema, description="Domain Admin group")
    def get(self, domain_id):
        try:
            return ADGroup.query.filter(
                and_(ADGroup.Domain_id == domain_id, ADGroup.SamAccountName == "Domain Admins")).first()
        except:
            abort(404, "Domain/Group not found.")



@blp.route("/domain/groups/by-name/")
class DomainGroupByNameView(MethodView):

    @blp.doc(description="Returns all groups that matches the name. If the id is also present in the search parameters "
                         "both values will be used.",
             summary="Find all domains that match the group name."
    )
    @blp.arguments(GroupNameSearchSchema, location="json", description="Attribute name specifies the group name or a "
                    "part of it. Attribute id is optional. If is present name and id will be used as filter, "
                    "otherwise the group is searched across all domains.")
    @blp.response(HTTPStatus.OK.value, ADGroupWithMembersSchema(many=True))
    def post(self, search_data):
        if "id" in search_data:
            groups = ADGroup.query.filter(
                and_(ADGroup.SamAccountName.like("%" + search_data['name'] + "%"),
                     ADGroup.Domain_id == search_data['id'])).all()
            return groups
        else:
            return ADGroup.query.filter(ADGroup.SamAccountName.like("%" + search_data['name'] + "%")).all()


@blp.route("/domain/<int:domain_id>/users/")
class DomainUserListView(MethodView):

    @blp.doc(description="Returns a list of all domain users for the domain with the specified ID.",
             summary="Find a list of all domain users for the domain with the specified ID."
             )
    @blp.response(HTTPStatus.OK.value, ADUserSchema(many=True), description="List of users in the domain. "
                                    "If no users are assigned to the domain an empty list is returned.")
    def get(self, domain_id):
        try:
            return ADUser.query.filter(ADUser.Domain_id == domain_id).all()
        except:
            abort(404, "Domain not found.")


@blp.route("/domain/<int:domain_id>/groups/")
class DomainGroupListView(MethodView):

    @blp.doc(description="Returns a list of all domain groups for the domain with the specified ID.",
             summary="Find a list of all domain groups for the domain with the specified ID."
             )
    @blp.response(HTTPStatus.OK.value, ADGroupSchema(many=True), description="List of groups in the domain. "
                                    "If no groups are assigned to the domain an empty list is returned")
    def get(self, domain_id):
        try:
            return ADGroup.query.filter(ADGroup.Domain_id == domain_id).all()
        except:
            abort(404, "Domain not found.")


@blp.route("/domain/<int:domain_id>/computers/")
class DomainComputerListView(MethodView):

    @blp.doc(description="Returns a list of all domain computers for the domain with the specified ID.",
             summary="Find a list of all domain computers for the domain with the specified ID."
             )
    @blp.response(HTTPStatus.OK.value, ADComputerSchema(many=True), description="List of computers in the domain. "
                                    "If no computers are assigned to the domain an empty list is returned")
    def get(self, domain_id):
        try:
            return ADComputer.query.filter(ADComputer.Domain_id == domain_id).all()
        except:
            abort(404, "Domain not found.")


@blp.route("/domain/<int:domain_id>/DCs/")
class DomainDCListView(MethodView):

    @blp.doc(description="Returns a list of all domain controllers for the domain with the specified ID.",
             summary="Find a list of all domain controllers for the domain with the specified ID."
             )
    @blp.response(HTTPStatus.OK.value, ADDomainControllerSchema(many=True), description="List of DCs in the domain. "
                                    "If no domain controllers are assigned to the domain an empty list is returned")
    def get(self, domain_id):
        try:
            return ADDomainController.query.filter(ADDomainController.Domain_id == domain_id).all()
        except:
            abort(404, "Domain not found.")


@blp.route("/domain/<int:domain_id>/pw-policies/")
class DomainPasswordPolicyListView(MethodView):

    @blp.doc(description="Returns a list of all password policies (default and fine grained) for the domain with "
                         "the specified ID.",
             summary="Find a list of all password policies for the domain with the specified ID."
             )
    @blp.response(HTTPStatus.OK.value, ADPasswordPolicySchema(many=True),
                  description="List of password policies in the domain. ")
    def get(self, domain_id):
        try:
            return ADPasswordPolicy.query.filter(ADPasswordPolicy.Domain_id == domain_id).all()
        except:
            abort(404, "Domain not found.")
