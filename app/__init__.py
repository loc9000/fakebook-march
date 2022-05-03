from flask import Flask
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    with app.app_context():
        from app.blueprints.main import bp as main_bp
        app.register_blueprint(main_bp)

        from app.blueprints.shop import bp as shop_bp
        app.register_blueprint(shop_bp)

        from app.blueprints.blog import bp as blog_bp
        app.register_blueprint(blog_bp)
        
        from app.blueprints.main import errors

    return app