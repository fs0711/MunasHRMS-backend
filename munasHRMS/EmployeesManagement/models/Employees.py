# Python imports

# Framework imports

# Local imports
from munasHRMS.generic import models
from munasHRMS.generic import db
from munasHRMS.generic.services.utils import constants, common_utils
from munasHRMS.UserManagement.models.User import User

class Employees(models.Model):
    @classmethod
    def validation_rules(cls):
        return {
            constants.EMPLOYEE__NAME: [{"rule": "required"}, {"rule": "datatype", "datatype": str}],
            constants.USER__PHONE_NUMBER: [
                {"rule": "datatype", "datatype": str},
                {
                    "rule": "unique",
                    "Model": cls,
                    "Field": constants.USER__PHONE_NUMBER,
                },
            ],
            # constants.EMPLOYEE__PHONE_NUMBER:  [{"rule": "datatype", "datatype": list},
            #                                     {"rule": "collection_format", "datatype": list,
            #                                 "validation_rules": [{"rule": "required"}, {"rule": "phone_number"}]}],
            constants.EMPLOYEE__EMAIL_ADDRESS: [{"rule": "email"}, {"rule": "datatype", "datatype": str}],
            constants.EMPLOYEE__ADDRESS: [{"rule": "datatype", "datatype": str}],
            constants.EMPLOYEE__GENDER: [{"rule": "choices", "options": constants.GENDER_LIST}],
            constants.EMPLOYEE__COUNTRY: [{"rule": "required"}, {"rule": "datatype", "datatype": str}],
            constants.EMPLOYEE__CITY: [{"rule": "required"}, {"rule": "datatype", "datatype": str}],
        }

    @classmethod
    def update_validation_rules(cls): return {
        constants.EMPLOYEE__NAME:[{"rule": "nonexistent"}],
        constants.EMPLOYEE__CITY:[{"rule": "nonexistent"}],
        constants.EMPLOYEE__COUNTRY:[{"rule": "nonexistent"}]
    }

    name = db.StringField(required=True)
    phone_number = db.StringField()
    email_address = db.StringField()
    address = db.StringField()
    gender = db.StringField()
    country = db.StringField(required=True)
    city = db.StringField(required=True)
    assigned_to = db.LazyReferenceField(User, required=True)
    assigned_by = db.LazyReferenceField(User, required=True)
    employee_id = db.SequenceField(value_decorator='EL-{}'.format)
    allocated_leaves = db.IntField(required=True)
    consumed_leaves = db.IntField(required=True)
    joining_date = db.IntField(required=True)
    probation_period = db.IntField(required=True)
    history = db.ListField(required=True)
    user_id = db.LazyReferenceField(User, required=True)
    custom_data = db.DictField(default={})

    def __str__(self):
        return str(self.pk)

    def display(self):
        return {
            constants.ID: str(self[constants.ID]),
            constants.EMPLOYEE__ID: self[constants.EMPLOYEE__ID],
            constants.EMPLOYEE__NAME: self[constants.EMPLOYEE__NAME],
            constants.EMPLOYEE__PHONE_NUMBER: self[constants.EMPLOYEE__PHONE_NUMBER],
            constants.EMPLOYEE__EMAIL_ADDRESS: self[constants.EMPLOYEE__EMAIL_ADDRESS],
            constants.EMPLOYEE__ADDRESS: self[constants.EMPLOYEE__ADDRESS],
            constants.EMPLOYEE__GENDER: self[constants.EMPLOYEE__GENDER],
            constants.EMPLOYEE__COUNTRY: self[constants.EMPLOYEE__COUNTRY],
            constants.EMPLOYEE__CITY: self[constants.EMPLOYEE__CITY],
            constants.EMPLOYEE__ASSIGNED_TO: self[constants.EMPLOYEE__ASSIGNED_TO].fetch().name,
            constants.EMPLOYEE__ASSIGNED_BY: self[constants.EMPLOYEE__ASSIGNED_BY].fetch().name,
            constants.STATUS: self[constants.STATUS],
            constants.CREATED_ON: self[constants.CREATED_ON],
            constants.UPDATED_ON: self[constants.UPDATED_ON],
            constants.EMPLOYEE__ALLOCATED_LEAVES: self[constants.EMPLOYEE__ALLOCATED_LEAVES],
            constants.EMPLOYEE__CONSUMED_LEAVES: self[constants.EMPLOYEE__CONSUMED_LEAVES],
            constants.EMPLOYEE__JOINING_DATE: self[constants.EMPLOYEE__JOINING_DATE],
            constants.EMPLOYEE__PROBATION_PERIOD: self[constants.EMPLOYEE__PROBATION_PERIOD],            
            constants.EMPLOYEE__HISTORY: self[constants.EMPLOYEE__HISTORY],
            constants.EMPLOYEE__CUSTOM_DATA:self[constants.EMPLOYEE__CUSTOM_DATA] if constants.EMPLOYEE__CUSTOM_DATA else {},
            'current': self[constants.EMPLOYEE__HISTORY][-1]
        }

    def display_min(self):
        return {
            constants.ID: str(self[constants.ID]),
            constants.EMPLOYEE__ID: self[constants.EMPLOYEE__ID],
            constants.EMPLOYEE__NAME: self[constants.EMPLOYEE__NAME],
            constants.EMPLOYEE__PHONE_NUMBER: self[constants.EMPLOYEE__PHONE_NUMBER],
            constants.EMPLOYEE__ASSIGNED_TO: self[constants.EMPLOYEE__ASSIGNED_TO].fetch().name,
            constants.CREATED_ON: common_utils.epoch_to_datetime(self[constants.CREATED_ON]),
        }