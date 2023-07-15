# Python imports

# Framework imports

# Local imports
from munasHRMS.generic import models
from munasHRMS.generic import db
from munasHRMS.generic.services.utils import constants, common_utils
from munasHRMS.config import config
from munasHRMS.ClientsManagement.models.Clients import Clients
from munasHRMS.ClientsManagement.models.Sites import Sites


class Schedule(models.Model):
    @classmethod
    def validation_rules(cls):
        return{
            constants.SCHEDULE__SITE:[{'rule':'required'}, {'rule':'datatype', 'datatype':str}],
            constants.SCHEDULE__CLIENT:[{'rule':'required'}, {'rule':'datatype', 'datatype':str}],
            constants.SCHEDULE__SCHEDULES:[{'rule':'required'}, {'rule':'datatype', 'datatype':list}],
            constants.SCHEDULE__DATE:[{'rule':'required'}, {'rule':'datatype', 'datatype':int}]
        }
    
    @classmethod
    def update_validation_rules(cls): return {
    }

    client = db.LazyReferenceField('Clients', required=True)
    site = db.LazyReferenceField('Sites', required=True)
    date = db.IntField(required=True)
    schedules=db.ListField(required=True)
    

    def __str__(self):
        return str(self.pk)


    def display(self):
        return {
            constants.ID:str(self[constants.ID]),
            constants.SCHEDULE__DATE: self[constants.SCHEDULE__DATE],
            constants.SCHEDULE__CLIENT: self[constants.SCHEDULE__CLIENT].fetch().name,
            constants.SCHEDULE__SITE: self[constants.SCHEDULE__SITE].fetch().name,
            constants.SCHEDULE__SCHEDULES: self[constants.SCHEDULE__SCHEDULES]
        }
