# Python imports
import os
import re
import pandas as pd
from datetime import datetime
# Framework imports
from flask import Blueprint, redirect, render_template, request

# Local imports
from munasHRMS.ProjectsManagement.controllers.ProjectController import ProjectController
from munasHRMS.OrganizationsManagement.controllers.organizationcontroller import OrganizationController
from munasHRMS.generic.services.utils import constants, decorators, common_utils, response_utils, response_codes
from munasHRMS.config import config

projects_bp = Blueprint("projects_bp", __name__)


@projects_bp.route("/create", methods=["POST"])
@decorators.is_authenticated
@decorators.keys_validator(
    constants.REQUIRED_FIELDS_LIST__PROJECTS,
    constants.OPTIONAL_FIELDS_LIST__PROJECTS,
    request_form_data=True
)
def create_organizations(data):
    res = ProjectController.create_controller(data=data)
    return render_template("addProject.html", **res)

@projects_bp.route("/create", methods=["GET"])
@decorators.is_authenticated
@decorators.keys_validator()
def create_organizations_veiw(data):
    res = {}
    res["organizations"] = OrganizationController.get_organizations()
    res =  response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=res)
    return render_template("addProject.html", **res)


@projects_bp.route("/read", methods=["GET"])
@decorators.is_authenticated
@decorators.keys_validator()
def read_view(data):
    res = ProjectController.read_controller(data=data)
    return render_template("viewProject.html", **res)


@projects_bp.route("/update", methods=["GET","POST"])
@decorators.is_authenticated
@decorators.keys_validator(
    [],
    constants.UPDATE_FIELDS_LIST__PROJECTS
)
def update_view(data):
    if request.method == "POST":
        res = ProjectController.update_controller(data)
        return redirect("/api/projects/read")
    data = request.args
    res = ProjectController.read_controller(data={constants.ID:data[constants.ID]})
    return render_template("editproject.html", **res)


@projects_bp.route("/suspend", methods=["GET"])
@decorators.is_authenticated
@decorators.keys_validator(
    [constants.ID],
    request_form_data=False
)
def suspend_view(data):
    res = ProjectController.suspend_controller(data)
    return redirect("/api/projects/read")
