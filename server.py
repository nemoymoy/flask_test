from flask import Flask, jsonify, request
from flask.views import MethodView
from models import User, Session
from errors import HttpError
from sqlalchemy.exc import IntegrityError
from schema import validate, CreateUserRequest, UpdateUserRequest
from flask_bcrypt import Bcrypt

app = Flask('app')
bcrypt = Bcrypt(app)

def hash_password(password: str) -> str:
    password = password.encode()
    password = bcrypt.generate_password_hash(password)
    password = password.decode()
    return password

@app.errorhandler(HttpError)
def error_handler(err: HttpError):
    http_response = jsonify({'error': err.message})
    http_response.status_code = err.status_code
    return http_response



@app.before_request
def before_request():
    session = Session()
    request.session = session

@app.after_request
def after_request(response):
    request.session.close()
    return response

def get_user_by_id(user_id: int):
    user = request.session.get(User, user_id)
    if user is None:
        raise HttpError(404, 'user not found')
    return user

def add_user(user: User):
    request.session.add(user)
    try:
        request.session.commit()
    except IntegrityError:
        raise HttpError(status_code=409, message='user with this login already exists')


class UserViews(MethodView):
    def get(self, user_id: int):
        user = get_user_by_id(user_id)
        return jsonify(user.json)

    def post(self):
        json_data = validate(CreateUserRequest, request.json)
        user = User(login=json_data['login'], password=hash_password(json_data['password']))
        add_user(user)
        return jsonify(user.id_json)

    def patch(self, user_id: int):
        json_data = validate(UpdateUserRequest, request.json)
        user = get_user_by_id(user_id)
        if 'login' in json_data:
            user.login = json_data['login']
        if 'password' in json_data:
            user.login = hash_password(json_data['password'])
        add_user(user)
        return jsonify(user.id_json)

    def delete(self, user_id: int):
        user = get_user_by_id(user_id)
        request.session.delete(user)
        request.session.commit()
        return jsonify({'status': 'delete'})

user_view = UserViews.as_view('user_view')

def hello_world(some_id):
    qs = request.args
    json_data = request.json
    headers = request.headers
    print(f'some_id: {some_id}')
    print(f'qs: {qs}')
    print(f'json_data: {json_data}')
    print(f'headers: {headers}')
    http_response = jsonify({'hello': 'world'})
    return http_response

app.add_url_rule(
    rule='/hello/world/<int:some_id>',
    view_func=hello_world,
    methods=['POST']
)

app.add_url_rule(
    rule='/users/<int:user_id>',
    view_func=user_view,
    methods=['GET', 'PATCH', 'DELETE']
)

app.add_url_rule(
    rule='/users',
    view_func=user_view,
    methods=['POST']
)

app.run()