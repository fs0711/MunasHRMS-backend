# Python imports

# Framework imports
from flask import jsonify


# Local imports
from munasHRMS import app, config
from munasHRMS.generic.services.utils import constants
from munasHRMS.UserManagement.views.users import users_bp
from munasHRMS.EmployeesManagement.views.employees import employees_bp
from munasHRMS.OrganizationsManagement.views.organizations import organizations_bp
from munasHRMS.ClientsManagement.views.clients import clients_bp
from munasHRMS.ClientsManagement.views.sites import sites_bp
from munasHRMS.SchedulesManagement.views.schedules import schedules_bp


@app.route("/api/static-data", methods=["GET"])
def static_data_view():
    return jsonify(constants.STATIC_DATA)


app.register_blueprint(users_bp, url_prefix="/api/users")
app.register_blueprint(organizations_bp, url_prefix="/api/organizations")
app.register_blueprint(clients_bp, url_prefix="/api/clients")
app.register_blueprint(sites_bp, url_prefix="/api/sites")
app.register_blueprint(employees_bp, url_prefix="/api/employees")
app.register_blueprint(schedules_bp, url_prefix="/api/schedules")
