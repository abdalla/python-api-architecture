from flask import request, jsonify, Blueprint, abort, g
from flask.views import MethodView
from app.views.auth import auth

from app import app

test = Blueprint('models', __name__)

@app.route('/test/home')
@app.route('/test/home/')
def home():
	return "Podemos por a lista de metodos aqui...."


class TestView(MethodView):
	@auth.login_required
	def get(self):
		return "COOL " + g.user.email


test_view = TestView.as_view('test_view')

app.add_url_rule(
	'/test/', view_func=test_view, methods=['GET']
)
