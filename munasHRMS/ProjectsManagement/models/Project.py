# Python imports

# Framework imports

# Local imports
from munasHRMS.generic import models
from munasHRMS.OrganizationsManagement.models.Organization import Organization
from munasHRMS.generic import db
from munasHRMS.generic.services.utils import constants, common_utils
from munasHRMS.config import config



class Project(models.Model):
    @classmethod
    def validation_rules(cls):
        return{
            constants.PROJECT__NAME:[{'rule':'required'}, {'rule':'datatype', 'datatype':str}],
            constants.PROJECT__ADDRESS:[{'rule':'required'}, {'rule':'datatype', 'datatype':str}],
            constants.PROJECT__CITY:[{'rule':'required'}, {'rule':'datatype', 'datatype':str}],
            constants.PROJECT__COUNTRY:[{'rule':'required'}, {'rule':'datatype', 'datatype':str}],
        }
    

    @classmethod
    def update_validation_rules(cls): return {
    }


    name = db.StringField(required=True)
    address = db.StringField(required=True)
    city = db.StringField(required=True)
    country = db.StringField(required=True)
    organization = db.LazyReferenceField('Organization', required=True)


    def __str__(self):
        return str(self.pk)


    def display(self):
        return {
            constants.ID:str(self[constants.ID]),
            constants.PROJECT__NAME: self[constants.PROJECT__NAME],
            constants.PROJECT__ADDRESS: self[constants.PROJECT__ADDRESS],
            constants.PROJECT__CITY: self[constants.PROJECT__CITY],
            constants.PROJECT__COUNTRY: self[constants.PROJECT__COUNTRY],
            constants.PROJECT__ORGANIZATION: self[constants.PROJECT__ORGANIZATION].fetch().name
        }