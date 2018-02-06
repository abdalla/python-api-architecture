from flask import g
from app import app, db
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from app.models.user import User


class Token(db.Model):
	__tablename__ = 'tokens'
	token_id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer)
	is_active = db.Column(db.Boolean)
	created_at = db.Column(db.DateTime, server_default=db.text("NOW()"))
	token = db.Column(db.String(140), index=True)

	def generate_auth_token(expiration=86400):
		s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
		return s.dumps({'user_id': g.user.user_id})

	@staticmethod
	def verify_auth_token(token):
		s = Serializer(app.config['SECRET_KEY'])
		print('>'*50)
		print(s)
		print(token)
		print(s.loads(token))

		# VALIDAR TOKEN AQUI por enquanto esta tudo em memoria... nao sei se vamos gravar em banco...

		try:
			data = s.loads(token)
		except SignatureExpired:
			return None  # valid token, but expired
		except BadSignature:
			return None  # invalid token
		user = User.query.get(data['user_id'])
		print(user.full_name)
		print('<' * 50)
		return user
