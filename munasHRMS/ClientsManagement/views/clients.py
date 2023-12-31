# Python imports
import os
import re
import pandas as pd
from datetime import datetime
# Framework imports
from flask import Blueprint, redirect, url_for, redirect, render_template, request

# Local imports
from munasHRMS.ClientsManagement.controllers.ClientsController import ClientsController
from munasHRMS.LeadsManagement.controllers.FollowUpController import FollowUpController
from munasHRMS.UserManagement.controllers.UserController import UserController
from munasHRMS.generic.services.utils import constants, decorators, common_utils
from munasHRMS.config import config

clients_bp = Blueprint("clients_bp", __name__)


@clients_bp.route("/create", methods=["POST"])
@decorators.is_authenticated
@decorators.keys_validator(
    constants.REQUIRED_FIELDS_LIST__CLIENTS,
    constants.OPTIONAL_FIELDS_LIST__CLIENTS,
    request_form_data=False
)
def leads_create_view(data):
    rest = ClientsController.create_controller(data=data)
    return (rest)


@clients_bp.route("/read", methods=["GET", "POST"])
@decorators.is_authenticated
@decorators.keys_validator()
def read_view(data):
    if request.method == "POST":
        data = request.form
    return ClientsController.read_controller(data=data)


@clients_bp.route("/getclients", methods=["GET"])
@decorators.is_authenticated
# @decorators.keys_validator()
def get_view():
    return ClientsController.get_clients()


@clients_bp.route("/update", methods=["PUT"])
@decorators.is_authenticated
# @decorators.roles_allowed([constants.ROLE_ID_ADMIN])
@decorators.keys_validator(
    [],
    constants.ALL_FIELDS_LIST__LEAD,
)
def update_view(data):
    return ClientsController.update_controller(data=data)

@clients_bp.route("/search", methods=["POST", "GET"])
@decorators.is_authenticated
@decorators.keys_validator()
def search_view(data):
    if request.method == "POST":
        data = request.form
        res = ClientsController.search_controller(data=data)
        return render_template("find_leads.html", **res)
    
    return render_template("find_leads.html")
