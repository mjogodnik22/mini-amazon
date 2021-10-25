from flask import Flask
from flask_login import LoginManager
from flask_babel import Babel
from .config import Config
from .db import DB


login = LoginManager()
login.login_view = 'users.login'
babel = Babel()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.db = DB(app)
    login.init_app(app)
    babel.init_app(app)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .users import bp as user_bp
    app.register_blueprint(user_bp)
    
    from .product_summaries import bp as product_summary_bp
    app.register_blueprint(product_summary_bp)
    
    from .add_new_product import bp as add_new_product_bp
    app.register_blueprint(add_new_product_bp)
    
    return app
