from flask import Flask
from config import Config
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

moment = Moment()
db = SQLAlchemy() # Object Relational Mapper
migrate = Migrate() # Handle Transaction for database
login = LoginManager() # handle login sessions
mail = Mail() # handle sending emails

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # tell my flask to use these services
    moment.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)

    # Flask Login configurations
    login.login_view = 'login'
    login.login_message = 'You do not have access to this page. Please log in.'
    login.login_message_category = 'danger'

    with app.app_context():
        from app.blueprints.main import bp as main_bp
        app.register_blueprint(main_bp)

        from app.blueprints.shop import bp as shop_bp
        app.register_blueprint(shop_bp)

        from app.blueprints.blog import bp as blog_bp
        app.register_blueprint(blog_bp)

        from app.contexts.cart import cart_context
        
        from app.blueprints.main import errors

    return app