from datetime import datetime

from backend.backend import db


class ModifiedMixin(object):
    created = db.DateTimeField()
    updated = db.DateTimeField()

    def save(self, *args, **kw):
        if self.id:
            self.updated = datetime.now()
        else:
            self.created = datetime.now()
            self.updated = self.created
        super(ModifiedMixin, self).save(*args, **kw)
