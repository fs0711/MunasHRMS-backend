# Python imports

# Framework imports

# Local imports
from munasHRMS.generic import models
from munasHRMS.generic import db
from munasHRMS.OrganizationsManagement.models import Organization
from munasHRMS.generic.services.utils import constants, common_utils
from munasHRMS.UserManagement.models.User import User

class Clients(models.Model):
    @classmethod
    def validation_rules(cls):
        return {
            constants.CLIENT__NAME: [{"rule": "required"}, {"rule": "datatype", "datatype": str}],
            constants.CLIENT__CP_PHONE_NUMBER:  [{"rule": "datatype", "datatype": list},
                                                {"rule": "collection_format", "datatype": list,
                                            "validation_rules": [{"rule": "required"}, {"rule": "phone_number"}]}],
            constants.CLIENT__CP_EMAIL: [{"rule": "email"}, {"rule": "datatype", "datatype": str}],
            constants.CLIENT__COUNTRY: [{"rule": "required"}, {"rule": "datatype", "datatype": str}],
            constants.CLIENT__CITY: [{"rule": "required"}, {"rule": "datatype", "datatype": str}],
            constants.CLIENT__ZIPCODE: [{"rule": "datatype", "datatype": str}],
            constants.CLIENT__CONTACT_PERSON: [{"rule": "datatype", "datatype": str}],
        }

    @classmethod
    def update_validation_rules(cls): return {

    }

    name = db.StringField(required=True)
    organization = db.LazyReferenceField(Organization, required=True)
    cp_phone_number = db.ListField()
    contact_person = db.StringField(required=True)
    country = db.StringField(required=True)
    city = db.StringField(required=True)
    zipcode = db.StringField(required=True)
    client_id = db.SequenceField(value_decorator='CL-{}'.format)

    def __str__(self):
        return str(self.pk)

    def display(self):
        return {
            constants.ID: str(self[constants.ID]),
            constants.CLIENT__ID: self[constants.CLIENT__ID],
            constants.CLIENT__NAME: self[constants.CLIENT__NAME],
            constants.CLIENT__CP_PHONE_NUMBER: self[constants.CLIENT__CP_PHONE_NUMBER],
            constants.CLIENT__CP_EMAIL: self[constants.CLIENT__CP_EMAIL],
            constants.CLIENT__COUNTRY: self[constants.CLIENT__COUNTRY],
            constants.CLIENT__CITY: self[constants.CLIENT__CITY],
            constants.CLIENT__CONTACT_PERSON: self[constants.CLIENT__CONTACT_PERSON],
            constants.STATUS: self[constants.STATUS],
            constants.CREATED_BY: self.created_by.fetch().name,
            constants.CREATED_ON: self[constants.CREATED_ON],
            constants.UPDATED_ON: self[constants.UPDATED_ON],
        }

    def display_min(self):
        return {
            constants.ID: str(self[constants.ID]),
            constants.CLIENT__ID: self[constants.CLIENT__ID],
            constants.CLIENT__NAME: self[constants.CLIENT__NAME],
            constants.CREATED_ON: common_utils.epoch_to_datetime(self[constants.CREATED_ON]),
        }