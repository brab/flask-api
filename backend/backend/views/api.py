from flask import Module, abort, jsonify, request
from flask.ext.login import current_user, login_user, logout_user
from flask.views import MethodView
from flask_mail import Message
from werkzeug import secure_filename

from backend.backend.decorators import jsonp
from backend.backend.models.my_model import MyModel
from backend.backend.models.user import User


api = Module(__name__, url_prefix='/api')

def jsonify_status_code(status_code, *args, **kw):
    response = jsonify(*args, **kw)
    response.status_code = status_code
    return response

@api.route('/')
def index():
    '''
    The root of the api returns an error
    '''
    abort(404)


class MyModelAPI(MethodView):
    @jsonp
    def get(self, id=None):
        if id:
            my_model = MyModel.objects.get(id=id)
            return jsonify(my_model=my_model.to_dict())
        else:
            my_models = MyModel.objects.all()
            my_models_list = [m.to_dict() for m in my_models]
            return jsonify(my_models=my_models_list)

    @jsonp
    def post(self):
        try:
            data = request.json
        except:
            return jsonify_status_code(400, message='Unable to decode data')

        value = data.get('value', '')

        my_model = MyModel.objects.create(value=value)

        return jsonify(my_model=my_model.to_dict())

    @jsonp
    def put(self, id):
        if not id:
            return jsonify_status_code(400, message='Id is required')

        try:
            data = request.json
        except:
            return jsonify_status_code(400, message='Unable to decode data')

        value = data.get('value', '')

        my_model = MyModel.objects.get(id=id)
        my_model.value = value
        my_model.save()

        return jsonify(my_model=my_model.to_dict())

    @jsonp
    def delete(self, id):
        if not id:
            return jsonify_status_code(400, message='Id is required')

        try:
            MyModel.objects.get(id=id).delete()
        except MyModel.DoesNotExist:
            return jsonify_status_code(410,
                    message='MyModel with id %s not found' % id)

        return jsonify_status_code(204, message='Deleted')

my_model_view = MyModelAPI.as_view('my_model_api')
api.add_url_rule('/my-model',
        view_func=my_model_view, methods=['GET', 'POST', ])
api.add_url_rule('/my-model/<string:id>',
        view_func=my_model_view, methods=['DELETE', 'GET', 'PUT', ])


class SessionAPI(MethodView):
    @jsonp
    def get(self):
        if not current_user.is_authenticated():
            return jsonify_status_code(410)
        return jsonify_status_code(200,
                username=current_user.username,
                email=current_user.email,
                admin=current_user.has_admin_access())

    @jsonp
    def post(self):
        try:
            data = request.json
        except:
            return jsonify_status_code(400, message='Unable to decode data')

        email_regex = r"[^@]+@[^@]+\.[^@]+"

        email = data.get('email', '').lower()
        password = data.get('password', '')

        if not re.match(email_regex, email):
            return jsonify_status_code(400,
                    message='Please enter a valid email address')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return jsonify_status_code(404,
                    message="That email's not in our system. Please try again")

        if not user.check_password(password):
            return jsonify_status_code(400, message='Invalid password')

        if login_user(user):
            return jsonify_status_code(201, admin=user.has_admin_access())
        else:
            return jsonify_status_code(400, message='User is inactive')

    @jsonp
    def delete(self):
        if not current_user.is_authenticated():
            abort(401)
        logout_user()
        return jsonify_status_code(204)

session_view = SessionAPI.as_view('session_api')
api.add_url_rule('/sessions',
        view_func=session_view, methods=['GET', 'POST', 'DELETE'])
