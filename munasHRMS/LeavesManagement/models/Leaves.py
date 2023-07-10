# Python imports

# Framework imports

# Local imports
from munasHRMS.generic import models
from munasHRMS.generic import db
from munasHRMS.generic.services.utils import constants, common_utils
from munasHRMS.UserManagement.models.User import User

class Leaves(models.Model):
    @classmethod
    def validation_rules(cls):
        return {
            constants.LEAVE__START: [{"rule": "required"}, {"rule": "date_format"}],
            constants.LEAVE__END: [{"rule": "required"}, {"rule": "date_format"}],
            constants.LEAVE__TYPE: [{"rule": "required"}, {"rule": "datatype", "datatype": str}],
        }

    @classmethod
    def update_validation_rules(cls):
        return {
            constants.LEAVE__START: [{"rule": "nonexistent"}],
            constants.LEAVE__END: [{"rule": "nonexistent"}],
            constants.LEAVE__TYPE: [{"rule": "nonexistent"}],
        }

    leave_start = db.IntField(required=True)
    leave_end = db.IntField(required=True)
    leave_type = db.StringField(required=True)
    note = db.StringField()
    deny_note = db.StringField()
    approved = db.BooleanField()
    reviewed = db.BooleanField()
    assigned_to = db.LazyReferenceField(User, required=True)
    assigned_by = db.LazyReferenceField(User, required=True)

    def __str__(self):
        return str(self.pk)

    def display(self):
        return {
            constants.ID: str(self[constants.ID]),
            constants.LEAVE__START: common_utils.epoch_to_datetime(self[constants.LEAVE__START]),
            constants.LEAVE__END: common_utils.epoch_to_datetime(self[constants.LEAVE__END]),
            constants.LEAVE__NOTE: self[constants.LEAVE__NOTE],
            constants.LEAVE__DNOTE: self[constants.LEAVE__DNOTE],
            constants.LEAVE__APPROVED: self[constants.LEAVE__APPROVED],
            constants.LEAVE__TYPE: self[constants.LEAVE__TYPE],
            constants.CREATED_BY: self.created_by.fetch().name,
            constants.LEAVE__REVIEWED: self[constants.LEAVE__REVIEWED]
        }