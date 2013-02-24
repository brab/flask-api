from flask.ext.admin import Admin
from flask.ext.admin.contrib.mongoengine import ModelView
from flask.ext.login import current_user

from backend.backend.models.my_model import MyModel
from backend.backend.models.user import User


class MyModelView(ModelView):
    can_create = True
    can_delete = True
    can_edit = True

    def __init__(self):
        super(MyModelView, self).__init__(
                model=MyModel, name='MyModels', endpoint='mymodels')

    def is_accessible(self):
        #return current_user.is_authenticated()
        return True


class UserView(ModelView):
    can_delete = False
    column_exclude_list = ('password', )
    form_excluded_columns = ('password', 'username', 'created', 'updated', )
    column_searchable_list = ('username', 'first_name', 'last_name', )

    def __init__(self):
        super(UserView, self).__init__(
                model=User, name='Users', endpoint='users')

    def is_accessible(self):
        #return current_user.is_authenticated()
        return True

admin = Admin(name='My App')

admin.add_view(MyModelView())
admin.add_view(UserView())
