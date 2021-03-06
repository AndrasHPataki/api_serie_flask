from flask import Blueprint, request, jsonify
from .models import Users, TokenBlacklist, many_users_schema
from flask_httpauth import HTTPBasicAuth
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity,get_raw_jwt
)
import datetime
from datetime import timedelta
#from .blacklist import blacklist

auth = HTTPBasicAuth()
main = Blueprint('main', __name__)

@auth.verify_password
def verify_password(username, password):
    checar_usuario = Users.query.filter_by(username=username).first()
    if checar_usuario and check_password_hash(checar_usuario.password, password):
        expires = datetime.timedelta(days=5)
        access_token = create_access_token(identity=str(checar_usuario.username), expires_delta=expires)
        return access_token
        
@main.route('/api/v1/login', methods=['GET', 'POST'])
@auth.login_required
def login():
    return jsonify({"message": auth.current_user()})

@main.route('/api/v1/seguro', methods=['GET'])
@jwt_required
def rota_segura():
    result = many_users_schema.dump(Users.query.all())
    return jsonify(result)
    #usuario_atual = get_jwt_identity()
    #return jsonify({"message": "Você esta protegido! {}".format(usuario_atual)})


@main.route('/api/v1/logout', methods=['GET', 'DELETE'])
@jwt_required
def logout_user():
    jti = get_raw_jwt()['jti']
    adicionar_token = TokenBlacklist(token=jti)
    db.session.add(adicionar_token)
    db.session.commit()
    return jsonify({"message": "Você Foi Deslogado!"})





@main.route('/api/v1/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        
        password = str(password)
        try:
            adicionar_user = Users(username=username,password=generate_password_hash(password,method='sha256'))
            db.session.add(adicionar_user)
            db.session.commit()
        except:
            return jsonify({"message": "Algo de errado.."})
        return jsonify({"message": "Usuário Cadastrado!"})
       
    return jsonify({"message": "Isso é um Get"})
