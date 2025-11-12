from flask import Flask, jsonify, request
from flask import MethodView
from models import User, Session

app = Flask('app')

class UserViews(MethodView):
    def get(self, user_id: int):
        with Session as session:
            user = session.get(User, user_id)
            if user:
                return jsonify({})
            else:
                http_response = jsonify({'error': 'user not found'})
                http_response.status_code = 404
                return http_response

    def post(self):
        json_data = request.json
        if 'login' not in json_data or 'password' not in json_data:
            http_response = jsonify({'error': 'bad request'})
            http_response.status_code = 400
            return http_response
        with Session as session:
            user = User(login=json_data['login'], password=json_data['password'])
            session.add(user)
            session.commit()
            return jsonify(user.id_json)

    def patch(self, user_id: int):
        json_data = request.json
        with Session as session:
            user = session.get(User, user_id)
            if user is None:
                http_response = jsonify({'error': 'user not found'})
                http_response.status_code = 404
                return http_response
            if 'login' in json_data:
                user.login = json_data['login']
            if 'password' in json_data:
                user.login = json_data['password']
            session.add(user)
            session.commit()
            return jsonify(user.id_json)

    def delete(self, user_id: int):
        with Session as session:
            user = session.get(User, user_id)
            if user is None:
                http_response = jsonify({'error': 'user not found'})
                http_response.status_code = 404
                return http_response
            session.delete(user)
            session.commit()
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
    rule='/users/<int:user_id>',
    view_func=user_view,
    methods=['POST']
)

app.run()