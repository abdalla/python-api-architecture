from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345@ali-mysql:3306/dev_cockpit'
app.config['SECRET_KEY'] = 'alibankeasycredit'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from app.views.user import user
from app.views.test import test
app.register_blueprint(user)

db.create_all()