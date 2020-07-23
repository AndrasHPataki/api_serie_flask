from .models import TokenBlacklist
from flask_jwt_extended import JWTManager
from . import db

def checar_token_valido(decrypted_token):
    jti = decrypted_token['jti']
    try:
        token = TokenBlacklist.query.filter_by(token=jti).first()
        if token:
            return jti
    except:
        return True
