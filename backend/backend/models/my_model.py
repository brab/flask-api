from backend.backend.models import db
from backend.backend.models.mixins import ModifiedMixin


class MyModel(ModifiedMixin, db.Document):
    value = db.StringField()

    def to_dict(self):
        return {
                'id': str(self.id),
                'created': self.created.strftime('%c'),
                'updated': self.updated.strftime('%c'),
                'value': self.value,
                }
