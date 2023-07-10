# Python imports
import os
import re
import pandas as pd
from datetime import datetime
# Framework imports
from flask import Blueprint, redirect, url_for, redirect, render_template, request

# Local imports
from munasHRMS.LeavesManagement.controllers.LeavesController import LeavesController
from munasHRMS.UserManagement.controllers.UserController import UserController
from munasHRMS.generic.services.utils import constants, decorators, common_utils
from munasHRMS.config import config

leaves_bp = Blueprint("leaves_bp", __name__)


@leaves_bp.route("/create", methods=["GET"])
@decorators.is_authenticated
def employees_create_view_get():
    return render_template("addemployee.html")

@leaves_bp.route("/create", methods=["POST"])
@decorators.is_authenticated
@decorators.keys_validator(
    constants.REQUIRED_FIELDS_LIST__LEAVE,
    request_form_data=False
)
def employees_create_view(data):
    rest = LeavesController.create_controller(data=data)
    return (rest)

@leaves_bp.route("/read", methods=["GET", "POST"])
@decorators.is_authenticated
@decorators.keys_validator()
def read_view(data):
    if request.method == "POST":
        data = request.form
    res = LeavesController.read_controller(data=data)
    return render_template("leaverequest.html", **res)


@leaves_bp.route("/update", methods=["POST"])
@decorators.is_authenticated
# @decorators.roles_allowed([constants.ROLE_ID_ADMIN])
@decorators.keys_validator(
    constants.UPDATE_FIELDS_LIST__LEAVE,
    request_form_data=False
)
def update_view(data):
    return LeavesController.update_controller(data=data)

@leaves_bp.route("/search", methods=["POST", "GET"])
@decorators.is_authenticated
@decorators.keys_validator()
def search_view(data):
    if request.method == "POST":
        data = request.form
        res = LeavesController.search_controller(data=data)
        return render_template("find_leads.html", **res)
    
    return render_template("find_leads.html")
