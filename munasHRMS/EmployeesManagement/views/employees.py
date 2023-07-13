# Python imports
import os
import re
import pandas as pd
from datetime import datetime
# Framework imports
from flask import Blueprint, redirect, url_for, redirect, render_template, request

# Local imports
from munasHRMS.EmployeesManagement.controllers.EmployeesController import EmployeesController
from munasHRMS.UserManagement.controllers.UserController import UserController
from munasHRMS.generic.services.utils import constants, decorators, common_utils
from munasHRMS.config import config

employees_bp = Blueprint("employees_bp", __name__)


@employees_bp.route("/create", methods=["POST"])
@decorators.is_authenticated
@decorators.keys_validator(
    constants.REQUIRED_FIELDS_LIST__EMPLOYEE,
    constants.OPTIONAL_FIELDS_LIST__EMPLOYEE
)
def employees_create_view(data):
    return EmployeesController.create_controller(data=data)


@employees_bp.route("/read", methods=["GET", "POST"])
@decorators.is_authenticated
@decorators.keys_validator()
def read_view(data):
    if request.method == "POST":
        data = request.form
    return EmployeesController.read_controller(data=data)


@employees_bp.route("/update", methods=["PUT"])
@decorators.is_authenticated
# @decorators.roles_allowed([constants.ROLE_ID_ADMIN])
@decorators.keys_validator(
    [],
    constants.REQUIRED_FIELDS_LIST__LEAVE,
)
def update_view(data):
    return EmployeesController.update_controller(data=data)


@employees_bp.route("/search", methods=["POST", "GET"])
@decorators.is_authenticated
@decorators.keys_validator()
def search_view(data):
    if request.method == "POST":
        data = request.form
    return EmployeesController.search_controller(data=data)