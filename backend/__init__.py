from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from backend.config import Config
from supabase import create_client, Client




db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
supabase: Client = None


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    global supabase
    if not supabase and app.config['SUPABASE_URL'] and app.config['SUPABASE_KEY']:
        supabase = create_client(app.config['SUPABASE_URL'], app.config['SUPABASE_KEY'])

    from backend.users.routes import users
    from backend.posts.routes import posts
    from backend.main.routes import main
    from backend.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app