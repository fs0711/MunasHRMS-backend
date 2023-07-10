# Python imports
import pandas as pd
import re
from math import nan, isnan
# Framework imports

# Local imports
from ast import Constant
from munasHRMS.generic.controllers import Controller
from munasHRMS.LeavesManagement.models.Leaves import Leaves
from munasHRMS.UserManagement.controllers.UserController import UserController
from munasHRMS.EmployeesManagement.controllers.EmployeesController import EmployeesController
from munasHRMS.generic.services.utils import constants, response_codes, response_utils, common_utils, pipeline
from munasHRMS import config
from datetime import datetime


class LeavesController(Controller):
    Model = Leaves

    @classmethod
    def create_controller(cls, data):
        is_valid, error_messages = cls.cls_validate_data(data=data)
        if not is_valid:
            return response_utils.get_response_object(
                response_code=response_codes.CODE_VALIDATION_FAILED,
                response_message=response_codes.MESSAGE_VALIDATION_FAILED,
                response_data=error_messages
            )
        current_user = common_utils.current_user()
        data[constants.EMPLOYEE__ASSIGNED_TO] = current_user
        data[constants.EMPLOYEE__ASSIGNED_BY] = current_user
        data[constants.LEAVE__START] = common_utils.convert_to_epoch1000(data[constants.LEAVE__START]+' 00:00:00', format=config.DATETIME_FORMAT)
        data[constants.LEAVE__END] = common_utils.convert_to_epoch1000(data[constants.LEAVE__END]+' 23:59:59', format=config.DATETIME_FORMAT)
        data[constants.LEAVE__APPROVED] = False
        data[constants.LEAVE__REVIEWED] = False

        _, _, obj = cls.db_insert_record(
            data=data, default_validation=False)
        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=obj.display()
        )

    @classmethod
    def read_controller(cls, data):
        filter = {}
        filter_data = {**data}
        filter_fields = {
            "project":constants.PROJECT,
            "level": constants.LEAD__LEVEL__LIST,
            "Task": constants.FOLLOW_UP__TYPE_LIST,
            "Next_task": constants.FOLLOW_UP__NEXT_TASK_LIST,
            "Team": [],
        }
        if data.get(constants.LEAD__ASSIGNED_TO):
            user_childs = [UserController.get_user(data.get(constants.LEAD__ASSIGNED_TO))]
            filter_data['assigned_to_name'] = user_childs[0]['name']
        else:
            user_childs = UserController.get_user_childs(
                user=common_utils.current_user(), return_self=True)

        user_ids = [id[constants.ID] for id in user_childs]
        filter[constants.EMPLOYEE__ASSIGNED_TO+"__in"] = [str(id) for id in user_ids]
        # filter[constants.LEAVE__REVIEWED] = False
        if data.get('page'):
            page = int(data['page'])
        else:
            page = 1
        
        if data.get('per_page'):
            per_page = int(data('per_page'))
        else:
            per_page = 50

        queryset = cls.db_read_records(read_filter={**filter}).paginate(page=page, per_page=per_page)
        leave_dataset = [obj.display() for obj in queryset.items]
        temp = UserController.get_user_childs(
            user=common_utils.current_user(), return_self=True)
        all_users = []
        for id in temp:
            all_users.append([str(id[constants.ID]) ,id[constants.USER__NAME]])
        leave_data = {}
        leave_data['data'] = leave_dataset
        leave_data['username'] = common_utils.current_user()[
            constants.USER__NAME]
        leave_data['userlevel'] = common_utils.current_user()[
            constants.USER__ROLE][constants.USER__ROLE__ROLE_ID]
        leave_data['all_users'] = all_users
        leave_data['pagination'] = {
            "next_num" : queryset.next_num,
            "page" : queryset.page,
            "pages" : queryset.pages,
            "per_page" : queryset.per_page,
            "prev_num" : queryset.prev_num,
            "total" : queryset.total,
            "has_next" : queryset.has_next,
            "has_prev" : queryset.has_prev
        }
        leave_data['filter_fields'] = filter_fields
        leave_data['filter_data'] = filter_data
        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=leave_data
        )

    @classmethod
    def update_controller(cls, data):
        if data['status'] == 'approve':
            queryset = cls.db_read_single_record(read_filter={constants.ID:data[constants.ID]})
            date_diff = queryset[constants.LEAVE__END]-queryset[constants.LEAVE__START]
            date_diff = ((date_diff/1000)/3600)
            date_diff = (int(date_diff) + bool(date_diff%1))//24
            queryset1 = EmployeesController.db_read_records(read_filter={constants.EMPLOYEE__USER_ID :str(queryset[constants.CREATED_BY].id)})
            employee_record = [obj.display() for obj in queryset1]
            history = employee_record[0][constants.EMPLOYEE__HISTORY].pop()
            history[constants.EMPLOYEE__CONSUMED_LEAVES] = history[constants.EMPLOYEE__CONSUMED_LEAVES] + date_diff
            history[constants.EMPLOYEE__REMAINING_LEAVES] = history[constants.EMPLOYEE__REMAINING_LEAVES] - date_diff
            employee_record[0][constants.EMPLOYEE__HISTORY].append(history)
            update_employee = {
                constants.EMPLOYEE__HISTORY: employee_record[0][constants.EMPLOYEE__HISTORY],
            }
            res = EmployeesController.db_update_single_record(read_filter={constants.ID:employee_record[0][constants.ID]}, update_filter=update_employee)
            update_data = {
                constants.LEAVE__APPROVED:True,
                constants.LEAVE__REVIEWED:True
            }
        if data['status'] == 'reject':
            update_data = {
                constants.LEAVE__APPROVED:False,
                constants.LEAVE__REVIEWED:True
            }

        is_valid, error_messages, obj = cls.db_update_single_record(
            read_filter={constants.ID: data[constants.ID]}, update_filter=update_data
        )
        if not is_valid:
            return response_utils.get_response_object(
                response_code=response_codes.CODE_VALIDATION_FAILED,
                response_message=response_codes.MESSAGE_VALIDATION_FAILED,
                response_data=error_messages
            )
        if not obj:
            return response_utils.get_response_object(
                response_code=response_codes.CODE_RECORD_NOT_FOUND,
                response_message=response_codes.MESSAGE_NOT_FOUND_DATA.format(
                    constants.LEAD.title(), constants.ID
                ))
        return response_utils.get_response_object(
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
            return response_utils.get_response_object(
                response_code=response_codes.CODE_SUCCESS,
                response_message=response_codes.MESSAGE_SUCCESS,
                response_data=obj.display(),
            )
        return response_utils.get_response_object(
            response_code=response_codes.CODE_RECORD_NOT_FOUND,
            response_message=response_codes.MESSAGE_NOT_FOUND_DATA.format(
                constants.LEAD.title(), constants.ID
            ))