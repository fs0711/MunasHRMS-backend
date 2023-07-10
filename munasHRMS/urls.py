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
from munasHRMS.EmployeesManagement.views.employees import employees_bp
from munasHRMS.OrganizationsManagement.views.organizations import organizations_bp
from munasHRMS.ClientsManagement.views.clients import clients_bp
from munasHRMS.generic.services.utils import common_utils
from munasHRMS.generic.services.utils.common_utils import current_user
from munasHRMS.LeadsManagement.controllers.DashboardController import DashboardController
from munasHRMS.LeadsManagement.controllers.DashboardController import DashboardFollow


@app.route("/api/static-data", methods=["GET"])
def static_data_view():
    return jsonify(constants.STATIC_DATA)


app.register_blueprint(users_bp, url_prefix="/api/users")
app.register_blueprint(organizations_bp, url_prefix="/api/organizations")
app.register_blueprint(clients_bp, url_prefix="/api/clients")
app.register_blueprint(employees_bp, url_prefix="/api/employees")
