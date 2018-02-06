from app import db
from passlib.apps import custom_app_context as pwd_context


class User(db.Model):
	__tablename__ = 'users'
	user_id = db.Column(db.Integer, primary_key=True)
	full_name = db.Column(db.String(150))
	email = db.Column(db.String(150), index=True)
	password = db.Column(db.String(128))
	cpf = db.Column(db.String(14), index=True)

	def __init__(self, name, email, cpf):
		self.full_name = name
		self.email = email
		self.cpf = cpf

	def __repr__(self):
		return '<User %d>' % self.user_id

	def hash_password(self, password):
		self.password = pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password, self.password)
