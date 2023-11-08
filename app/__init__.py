from app.config import Config
from app.api.key_routes import key_routes
from app.api.auth_routes import auth_routes
from app.api.product_routes import product_routes

from .models import db, User


from flask import Flask
from flask_login import LoginManager
from flask_swagger_ui import get_swaggerui_blueprint


app = Flask(__name__)
app.config.from_object(Config)

lm = LoginManager(app)
lm.init_app(app)
lm.login_view = 'login_page'

db.init_app(app)


### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "License Manager"
    }
)

app.register_blueprint(auth_routes, url_prefix='/api/auth')
app.register_blueprint(key_routes, url_prefix='/api/keys')
app.register_blueprint(product_routes, url_prefix='/api/products')
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from app import views