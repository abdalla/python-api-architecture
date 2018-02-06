import json
from flask import request, jsonify, Blueprint, abort, g
from flask.views import MethodView
from app import db, app
from app.views.auth import auth
from app.models.token import Token
from app.models.user import User

user = Blueprint('models', __name__)


@user.route('/users/home')
def home():
	return "Podemos por a lista de metodos aqui...."


@auth.verify_password
def verify_password(userEmail, pwd):
	token = request.headers.get('token')

	user = None

	if token:
		# first try to authenticate by token
		user = Token.verify_auth_token(token)

	if not user:
		json_data = request.get_json()

		if not json_data:
			return False

		email = json_data["email"]
		password = json_data["password"]
		# try to authenticate with useremail/password
		user = User.query.filter_by(email=email).first()
		if not user or not user.verify_password(password):
			return False

	g.user = user

	return True


class UserView(MethodView):
	@auth.verify_password
	def verify_password(userEmail, pwd):
		token = request.headers.get('token')

		user = None

		if token:
			# first try to authenticate by token
			user = Token.verify_auth_token(token)

		if not user:
			json_data = request.get_json()

			if not json_data:
				return False

			email = json_data["email"]
			password = json_data["password"]
			# try to authenticate with useremail/password
			user = User.query.filter_by(email=email).first()
			if not user or not user.verify_password(password):
				return False

		g.user = user

		return True

	@auth.login_required
	def get(self, id=None, page=1):
		if not id:
			users = User.query.paginate(page, 10).items
			res = {}
			for user in users:
				res[user.user_id] = {
					'full_name': user.full_name
				}
		else:
			user = User.query.filter_by(user_id=id).first()
			if not user:
				abort(404)
			res = {
				'full_name': user.full_name
			}
		return jsonify(res)

	def post(self):
		json_data = request.get_json(force=True)
		full_name = json_data["full_name"]
		email = json_data["email"]
		password = json_data["password"]
		cpf = json_data["cpf"]

		if email is None or password is None or cpf is None:
			abort(400)  # missing arguments
		if User.query.filter_by(email=email).first() is not None:
			abort(400)  # existing user
		if User.query.filter_by(cpf=cpf).first() is not None:
			abort(400)  # existing user

		user = User(full_name, email, cpf)
		user.hash_password(password)

		db.session.add(user)
		db.session.commit()
		return jsonify({user.user_id: {
			'full_name': user.full_name
		}})

	@auth.login_required
	def put(self, id):
		# Update the record for the provided id
		# with the details provided.
		return

	@auth.login_required
	def delete(self, id):
		user = User.query.filter_by(user_id=id).first()
		db.session.delete(user)
		db.session.commit()
		return jsonify({
			'mesage': 'Usário deletado com sucesso'
		})


user_view = UserView.as_view('user_view')

app.add_url_rule(
	'/users/', view_func=user_view, methods=['GET', 'POST']
)
app.add_url_rule(
	'/users/<int:id>', view_func=user_view, methods=['GET', 'DELETE', 'PUT']
)


@app.route('/users/token', methods=['POST'])
@auth.login_required
def get_auth_token():
	token = Token.generate_auth_token()
	return jsonify({'token': token.decode('ascii')})
