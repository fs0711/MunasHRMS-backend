# Python imports
from math import nan, isnan
# Framework imports
from flask_mongoengine import pagination
# Local imports
from ast import Constant
from munasHRMS.generic.controllers import Controller
from munasHRMS.LeadsManagement.models.CallRecord import CallRecords
from munasHRMS.LeadsManagement.controllers.LeadsController import LeadsController
from munasHRMS.UserManagement.controllers.UserController import UserController
from munasHRMS.generic.services.utils import constants, response_codes, response_utils, common_utils, pipeline
from munasHRMS import config
from datetime import datetime, timedelta


class CallRecordController(Controller):
    Model = CallRecords

    @classmethod
    def create_controller(cls, data):
        is_valid, error_messages = cls.cls_validate_data(data=data)
        if not is_valid:
            return response_utils.get_response_object(
                response_code=response_codes.CODE_VALIDATION_FAILED,
                response_message=response_codes.MESSAGE_VALIDATION_FAILED,
                response_data=error_messages
            )
        if data[constants.CALL_RECORD__PHONE_NUMBER].find('03') == 0:
            data[constants.CALL_RECORD__PHONE_NUMBER] = "+92" + data[constants.CALL_RECORD__PHONE_NUMBER][1:]
        if data[constants.CALL_RECORD__PHONE_NUMBER].find('02') == 0:
            data[constants.CALL_RECORD__PHONE_NUMBER] = "+92" + data[constants.CALL_RECORD__PHONE_NUMBER][1:]
        already_exist = cls.db_read_single_record(read_filter={constants.CALL_RECORD__DATE:data[constants.CALL_RECORD__DATE], constants.CALL_RECORD__PHONE_NUMBER:data[constants.CALL_RECORD__PHONE_NUMBER]})
        if not already_exist:
            queryset = LeadsController.db_read_records(read_filter={
                constants.LEAD__PHONE_NUMBER+"__in": [data[constants.CALL_RECORD__PHONE_NUMBER]],
                # constants.CREATED_BY+"__nin": [current_user]
            })
            if (queryset):
                for obj in queryset:
                    lead = obj.display() 
                data.update({constants.CALL_RECORD__LEAD_ID:lead[constants.ID]})
                _, _, obj = cls.db_insert_record(
                    data=data, default_validation=False)
                return response_utils.get_response_object(
                    response_code=response_codes.CODE_SUCCESS,
                    response_message=response_codes.MESSAGE_SUCCESS,
                )
            return response_utils.get_response_object(
                response_code=response_codes.CODE_CREATE_FAILED,
                response_message=response_codes.MESSAGE_INVALID_PHONENUMBER,
            )
        return response_utils.get_response_object(
            response_code=response_codes.CODE_CREATE_FAILED,
            response_message=response_codes.MESSAGE_DUPLICATE_ENTRY,
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
        queryset = cls.db_read_records(read_filter={**filter}).order_by('-id').paginate(page=page, per_page=per_page)
        if data.get('edit'):
            lead_dataset = [obj.display_edit() for obj in queryset.items]
        else:
            lead_dataset = [obj.display_min() for obj in queryset.items]
        temp = UserController.get_user_childs(
            user=common_utils.current_user(), return_self=True)
        all_users = []
        for id in temp:
            all_users.append([str(id[constants.ID]) ,id[constants.USER__NAME]])
        leads_data = {}
        leads_data['data'] = lead_dataset
        leads_data['username'] = common_utils.current_user()[
            constants.USER__NAME]
        leads_data['userlevel'] = common_utils.current_user()[
            constants.USER__ROLE][constants.USER__ROLE__ROLE_ID]
        leads_data['all_users'] = all_users
        leads_data['pagination'] = {
            "next_num" : queryset.next_num,
            "page" : queryset.page,
            "pages" : queryset.pages,
            "per_page" : queryset.per_page,
            "prev_num" : queryset.prev_num,
            "total" : queryset.total,
            "has_next" : queryset.has_next,
            "has_prev" : queryset.has_prev
        }
        leads_data['filter_fields'] = filter_fields
        leads_data['filter_data'] = filter_data
        return response_utils.get_response_object(
            response_code=response_codes.CODE_SUCCESS,
            response_message=response_codes.MESSAGE_SUCCESS,
            response_data=leads_data
        )
    
    @classmethod
    def read_basic_report(cls, data):
        filter = {}
        filter_data = {**data}
        if data.get(constants.DATE_FROM):
            datefrom = data.get(constants.DATE_FROM) + ' 00:00:00'
            dateto = data.get(constants.DATE_TO) + ' 23:59:59'
            filter[constants.CREATED_ON +
                   "__gte"] = common_utils.convert_to_epoch1000(datefrom, format=config.FILTER_DATETIME_FORMAT)
            filter[constants.CREATED_ON +
                   "__lte"] = common_utils.convert_to_epoch1000(dateto, format=config.FILTER_DATETIME_FORMAT)
            datefrom = datefrom[:11]
            dateto = dateto[:11]
        else:
            datefrom = datetime.combine(datetime.now().date(), time(
                0, 0)).strftime(config.DATETIME_FORMAT)
            dateto = datetime.combine(datetime.now().date(), time(
                23, 59, 59)).strftime(config.DATETIME_FORMAT)
            filter[constants.CREATED_ON +
                   "__gte"] = common_utils.convert_to_epoch1000(datefrom)
            filter[constants.CREATED_ON +
                   "__lte"] = common_utils.convert_to_epoch1000(dateto)
            datefrom = datetime.now().date().strftime("%d %m %Y")
            dateto = datetime.now().date().strftime("%d %m %Y")

        if data.get(constants.LEAD__ASSIGNED_TO):
            user_childs = [UserController.get_user(
                data.get(constants.CREATED_BY))]
        else:
            user_childs = UserController.get_user_childs(
                user=common_utils.current_user(), return_self=True)
        user_ids = [id[constants.ID] for id in user_childs]
        # user_ids = [id(constants.ID) for id in user_childs]

        filter[constants.CREATED_BY+"__in"] = [str(id) for id in user_ids]
        queryset = cls.db_read_records(read_filter={**filter}).aggregate(
            pipeline.KPI_REPORT_FOLLOW_UP)