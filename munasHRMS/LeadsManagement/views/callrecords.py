# Python imports
import os
import re
import pandas as pd
from datetime import datetime
# Framework imports
from flask import Blueprint, redirect, url_for, redirect, render_template, request

# Local imports
from munasHRMS.LeadsManagement.controllers.CallRecordController import CallRecordController
from munasHRMS.generic.services.utils import constants, decorators, common_utils
from munasHRMS.config import config

calls_bp = Blueprint("calls_bp", __name__)

    
@calls_bp.route("/verify", methods=["POST"])
@decorators.is_authenticated
@decorators.keys_validator(
    constants.REQUIRED_FIELDS_LIST__CALL_RECORDS,
    [constants.CALL_RECORD__LOCALE],
    request_form_data=False
)
def calls_verify_view(data):
    res = CallRecordController.create_controller(data=data)
    return res

# @calls_bp.route("/read", methods=["GET", "POST"])
# @decorators.is_authenticated
# # @decorators.roles_allowed([constants.ROLE_ID_ADMIN])
# # @decorators.keys_validator()
# def read_view():
#     if request.method == "POST":
#         data = request.form
#         res = LeadsController.read_controller(data=data)
#         return res    
#     data = request.args
#     res = LeadsController.read_controller(data=data)
#     return render_template("viewleads.html", **res)

# @calls_bp.route("/update", methods=["GET","POST"])
# @decorators.is_authenticated
# @decorators.keys_validator(
#     [],
#     constants.ALL_FIELDS_LIST__LEAD,
#     request_form_data=False
# )
# def update_view(data):
#     if request.method == "POST":
#         # data = request.form
#         res = LeadsController.update_controller(data=data)
#         return render_template("editlead.html", **res)
#     data = request.args
#     res = LeadsController.read_controller(data=data)
#     return render_template("editlead.html", **res)

# @calls_bp.route("/search", methods=["POST", "GET"])
# @decorators.is_authenticated
# @decorators.keys_validator()
# def search_view(data):
#     if request.method == "POST":
#         data = request.form
#         res = LeadsController.search_controller(data=data)
#         return render_template("find_leads.html", **res)
    
#     return render_template("find_leads.html")
