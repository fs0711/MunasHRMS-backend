# Python imports
import pandas as pd
import re
from math import nan, isnan
# Framework imports

# Local imports
from ast import Constant
from munasHRMS.generic.controllers import Controller
from munasHRMS.EmployeesManagement.models.Employees import Employees
from munasHRMS.UserManagement.controllers.UserController import UserController
from munasHRMS.generic.services.utils import constants, response_codes, response_utils, common_utils, pipeline
from munasHRMS import config
from datetime import datetime, timedelta


class EmployeesController(Controller):
    Model = Employees

    @classmethod
    def create_controller(cls, data):
        is_valid, error_messages = cls.cls_validate_data(data=data)
        if not is_valid:
            return response_utils.get_json_response_object(
                response_code=response_codes.CODE_VALIDATION_FAILED,
                response_message=response_codes.MESSAGE_VALIDATION_FAILED,
                response_data=error_messages
            )
        current_user = common_utils.current_user()
        already_exists = cls.db_read_records(read_filter={
            constants.EMPLOYEE__PHONE_NUMBER: data[constants.EMPLOYEE__PHONE_NUMBER],
        })
        if already_exists:
            return response_utils.get_json_response_object(
                response_code=response_codes.CODE_USER_ALREADY_EXIST,
                response_message=response_codes.MESSAGE_ALREADY_EXISTS_DATA,
                response_data=already_exists
            )
        user_data = {
            constants.USER__NAME:data[constants.EMPLOYEE__NAME],
            constants.USER__EMAIL_ADDRESS:data[constants.EMPLOYEE__EMAIL_ADDRESS],
            constants.USER__GENDER:data[constants.EMPLOYEE__GENDER],
            constants.USER__PASSWORD:data[constants.USER__PASSWORD],
            constants.USER__ROLE:data[constants.USER__ROLE],
            constants.USER__MANAGER:data[constants.USER__MANAGER],
            constants.USER__ORGANIZATION:data[constants.USER__ORGANIZATION],
            constants.EMPLOYEE__PHONE_NUMBER:data[constants.EMPLOYEE__PHONE_NUMBER]
            }
              
        res = UserController.create_controller(user_data)
        res = res.json
        if res['response_code'] == 200:
            print(res['response_data'])
            del data[constants.USER__PASSWORD]
            del data[constants.USER__ROLE]
            del data[constants.USER__MANAGER]
            del data[constants.USER__ORGANIZATION]
            data[constants.EMPLOYEE__USER_ID] = res['response_data']['id']
            data[constants.EMPLOYEE__JOINING_DATE] = data[constants.EMPLOYEE__JOINING_DATE] * 1000
            cycle_date = data[constants.EMPLOYEE__JOINING_DATE] + (data[constants.EMPLOYEE__PROBATION_PERIOD] * 24 * 60*60*1000)
            data[constants.EMPLOYEE__HISTORY] = [{
                "year":datetime.today().year,
                "cycle_date":cycle_date,
                constants.EMPLOYEE__ALLOCATED_LEAVES:int(data[constants.EMPLOYEE__ALLOCATED_LEAVES]),
                constants.EMPLOYEE__CONSUMED_LEAVES:int(data[constants.EMPLOYEE__CONSUMED_LEAVES]),
                "remaining":int(data[constants.EMPLOYEE__ALLOCATED_LEAVES])-int(data[constants.EMPLOYEE__CONSUMED_LEAVES])
            }]
            _, _, obj = cls.db_insert_record(
                data=data, default_validation=False)
            return response_utils.get_json_response_object(
                response_code=response_codes.CODE_SUCCESS,
                response_message=response_codes.MESSAGE_SUCCESS,
                response_data=obj.display()
            )
        else:
            return response_utils.get_json_response_object(
                response_code=res['response_code'],
                response_message=res['response_message'],
                response_data=res['response_data']
            )

    @classmethod
    def read_controller(cls, data): 
        filter = {}
        if data.get(constants.ASSIGNED_TO):
            user_childs = [UserController.get_user(data.get(constants.ASSIGNED_TO))]
        else:
            user_childs = UserController.get_user_childs(
                user=common_utils.current_user(), return_self=True)

        user_ids = [id[constants.ID] for id in user_childs]
        filter[constants.ASSIGNED_TO+"__in"] = [str(id) for id in user_ids]
        if data.get('page'):
            page = int(data['page'])
        else:
            page = 1
        
        if data.get('per_page'):
            per_page = int(data('per_page'))
        else:
            per_page = 50

        queryset = cls.db_read_records(read_filter={**filter}).order_by('-id').paginate(page=page, per_page=per_page)
        employee_dataset = [obj.display() for obj in queryset.items]

        return response_utils.get_json_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=employee_dataset
        )

    @classmethod
    def update_controller(cls, data):
        is_valid, error_messages, obj = cls.db_update_single_record(
            read_filter={constants.ID: data[constants.ID]}, update_filter=data
        )
        if not is_valid:
            return response_utils.get_json_response_object(
                response_code=response_codes.CODE_VALIDATION_FAILED,
                response_message=response_codes.MESSAGE_VALIDATION_FAILED,
                response_data=error_messages
            )
        if not obj:
            return response_utils.get_json_response_object(
                response_code=response_codes.CODE_RECORD_NOT_FOUND,
                response_message=response_codes.MESSAGE_NOT_FOUND_DATA.format(
                    constants.LEAD.title(), constants.ID
                ))
        return response_utils.get_json_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=obj.display(),
        )

    @classmethod
    def suspend_controller(cls, data):
        _, _, obj = cls.db_update_single_record(
            read_filter={constants.ID: data[constants.ID]},
            update_filter={
                constants.STATUS: constants.OBJECT_STATUS_SUSPENDED},
            update_mode=constants.UPDATE_MODE__PARTIAL,
        )
        if obj:
            return response_utils.get_json_response_object(
                response_code=response_codes.CODE_SUCCESS,
                response_message=response_codes.MESSAGE_SUCCESS,
                response_data=obj.display(),
            )
        return response_utils.get_json_response_object(
            response_code=response_codes.CODE_RECORD_NOT_FOUND,
            response_message=response_codes.MESSAGE_NOT_FOUND_DATA.format(
                constants.LEAD.title(), constants.ID
            ))
