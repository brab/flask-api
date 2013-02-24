from flask.ext.login import UserMixin

from backend.backend.models import db
from backend.backend.models.mixins import ModifiedMixin


class User(ModifiedMixin, db.Document, UserMixin):
    username = db.StringField(unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(default='!')
    first_name = db.StringField()
    last_name = db.StringField()

    is_active = db.BooleanField(default=True)
    is_staff = db.BooleanField(default=False)
    is_superuser = db.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.email

    def save(self, *args, **kw):
        if not self.username:
            self.username = self.email[:self.email.find('@')]
        super(self.__class__, self).save(*args, **kw)

    def check_password(self, password):
        '''
        Populate this method to properly check passwords for your system
        '''
        return True

    def set_password(self, password):
        '''
        Populate this method to set user passwords with encryption
        '''
        return True
