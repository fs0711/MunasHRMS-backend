# Python imports

# Framework imports

# Local imports
from munasHRMS.generic import models
from munasHRMS.generic import db
from munasHRMS.generic.services.utils import constants, common_utils
from munasHRMS.LeadsManagement.models.Lead import Leads
from munasHRMS.config import config

class CallRecords(models.Model):
    @classmethod
    def validation_rules(cls):
        return {
            constants.CALL_RECORD__DATE: [{"rule": "required"}, {"rule": "datatype", "datatype": int}],
            constants.CALL_RECORD__LOCALE: [{"rule": "datatype", "datatype": str}],
            constants.CALL_RECORD__TYPE: [{"rule": "required"}, {"rule": "datatype", "datatype": str}],
            constants.CALL_RECORD__DURATION: [{"rule": "required"}, {"rule": "datatype", "datatype": int}],
            constants.CALL_RECORD__PHONE_NUMBER: [{"rule": "required"}, {"rule": "phone_number"}, {"rule": "datatype", "datatype": str}],
        }

    @classmethod
    def update_validation_rules(cls): return {
    }

    phone_number = db.StringField(required=True)
    call_date = db.IntField(required=True)
    call_duration = db.IntField(required=True)
    call_type = db.StringField(required=True)
    call_locale = db.StringField()
    lead_id = db.LazyReferenceField(Leads, required=True)
    call_id = db.SequenceField(value_decorator='CA-{}'.format)

    def __str__(self):
        return str(self.pk)

    def display(self):
        return {
            constants.ID: str(self[constants.ID]),
            constants.CALL_RECORD__DATE: self[constants.CALL_RECORD__DATE],
            constants.CALL_RECORD__TYPE: self[constants.CALL_RECORD__TYPE],
            constants.CALL_RECORD__DURATION: self[constants.CALL_RECORD__DURATION],
            constants.CALL_RECORD__PHONE_NUMBER: self[constants.CALL_RECORD__PHONE_NUMBER],
            constants.CALL_RECORD__LEAD_ID: self[constants.CALL_RECORD__LEAD_ID].fetch().display()
        }
