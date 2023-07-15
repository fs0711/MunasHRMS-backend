# Python imports
import os
import re
import pandas as pd
from datetime import datetime
# Framework imports
from flask import Blueprint, redirect, request

# Local imports
from munasHRMS.SchedulesManagement.controllers.schedulescontroller import ScheduleController
from munasHRMS.generic.services.utils import constants, decorators, common_utils
from munasHRMS.config import config

schedules_bp = Blueprint("schedules_bp", __name__)


@schedules_bp.route("/create", methods=["POST"])
@decorators.is_authenticated
@decorators.keys_validator(
constants.REQUIRED_FIELDS_LIST__ORGANIZATION,
    constants.OPTIONAL_FIELDS_LIST__ORGANIZATION,
    request_form_data=False
)
def create_view(data):
    res = ScheduleController.create_controller(data=data)
    return res


@schedules_bp.route("/read", methods=["GET"])
@decorators.is_authenticated
@decorators.keys_validator()
def read_view(data):
    return ScheduleController.read_controller(data=data)


@schedules_bp.route("/update", methods=["POST"])
@decorators.is_authenticated
@decorators.keys_validator(
    [],
    constants.UPDATE_FIELDS_LIST__ORGANIZATION,
    request_form_data=False
)
def update_view(data):
    return ScheduleController.read_controller(data={constants.ID:data[constants.ID]})


@schedules_bp.route("/suspend", methods=["GET"])
@decorators.is_authenticated
@decorators.keys_validator(
    [constants.ID],
    request_form_data=False
)
def suspend_view(data):
    res = ScheduleController.suspend_controller(data)
    return redirect("/api/organizations/read")

    
        




