from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

ma = Marshmallow()
db = SQLAlchemy()


from .blacklist import checar_token_valido
def create_app(config_file='settings.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    db.init_app(app)
    ma.init_app(app)
    migrate = Migrate(app, db)
    
    from .models import Users, TokenBlacklist, Products
    from .main import main
    from .product_api import api_produtos
    jwt = JWTManager(app)
    app.register_blueprint(main)
    app.register_blueprint(api_produtos)
    
    
    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        return checar_token_valido(decrypted_token)
        #jti = decrypted_token['jti']
        #print(decrypted_token)
        #return jti in blacklist
    
    @jwt.revoked_token_loader
    def invalid_acess_token():
        return "Token Invalido"
    return app
