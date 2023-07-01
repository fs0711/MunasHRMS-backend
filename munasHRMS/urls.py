# Python imports

# Framework imports
from flask import jsonify
from flask import render_template, redirect, request, Response
from datetime import datetime, timedelta

# Local imports
from munasHRMS import app, config
from munasHRMS.LeadsManagement.controllers.LeadsController import LeadsController
from munasHRMS.generic.services.utils import constants, decorators
from munasHRMS.UserManagement.views.users import users_bp
from munasHRMS.LeadsManagement.views.leads import leads_bp
from munasHRMS.OrganizationsManagement.views.organizations import organizations_bp
from munasHRMS.LeadsManagement.views.follow_ups import follow_ups_bp
from munasHRMS.LeadsManagement.views.reports import reports_bp
from munasHRMS.LeadsManagement.views.callrecords import calls_bp
from munasHRMS.ClientsManagement.views.clients import clients_bp
from munasHRMS.ProjectsManagement.views.projects import projects_bp
from munasHRMS.generic.services.utils import common_utils
from munasHRMS.generic.services.utils.common_utils import current_user
from munasHRMS.LeadsManagement.controllers.DashboardController import DashboardController
from munasHRMS.LeadsManagement.controllers.DashboardController import DashboardFollow


@app.route("/home", methods=["GET"])
# @decorators.logging
@decorators.is_authenticated
@decorators.keys_validator(
    [],
    constants.ALL_FIELDS_LIST__LEAD,
)
def dashboard_view(data):
    res = DashboardController.get_dashboard_stats()
    return render_template('dashboard.html', **res)


@app.route("/addlead", methods=["GET"])
def addlead_view():
    return render_template('addlead.html')

@app.route("/api/static-data", methods=["GET"])
def static_data_view():
    return jsonify(constants.STATIC_DATA)


app.register_blueprint(users_bp, url_prefix="/")
app.register_blueprint(leads_bp, url_prefix="/api/leads")
app.register_blueprint(organizations_bp, url_prefix="/api/organizations")
app.register_blueprint(follow_ups_bp, url_prefix="/api/follow_ups")
app.register_blueprint(reports_bp, url_prefix="/api/reports")
app.register_blueprint(clients_bp, url_prefix="/api/clients")
app.register_blueprint(calls_bp, url_prefix="/api/calls")
app.register_blueprint(projects_bp, url_prefix="/api/projects")
