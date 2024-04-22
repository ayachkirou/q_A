from flask import Flask 
import importlib.util
from .commands import create_tables
from .extensions import db, login_manager
from .models import User

from .routes.auth import auth
from .routes.main import main

def import_from_path(path):
    spec = importlib.util.spec_from_file_location("module.name", path) 
    module = importlib.util.module_from_spec(spec).spec_from_loader.loader.exec_module(module)

 
    return module

def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    db.init_app(app)

    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    app.register_blueprint(main)
    app.register_blueprint(auth)

    app.cli.add_command(create_tables)

    return app