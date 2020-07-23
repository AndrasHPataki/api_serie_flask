from flask import Blueprint, request, jsonify
from .models import Products,many_products_schema,one_product_schema

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity,get_raw_jwt
)

from .controllers import ProductResult
api_produtos = Blueprint('api_produtos', __name__)

#DEFINIR PRIMEIRO ENDPOINT -> GET = PASSAR PARAMETROS PELA URL
@api_produtos.route('/api/v1/produtos')
def get_produtos():
    try:
        result = many_products_schema.dump(Products.query.all())
        return jsonify(result)
    except:
        return jsonify({"message": "Houve algum Erro!"})

@api_produtos.route('/api/v1/produtos/<int:id_produto>')
def get_produtos_por_id(id_produto):
    try:
        result = one_product_schema.dump(Products.query.filter_by(id=id_produto).first())
        return jsonify(result)
    except:
        return jsonify({"message": "Houve algum Erro!"})



@api_produtos.route('/api/v1/post/produtos', methods=['GET', 'POST'])
@jwt_required
def post_produtos():
    if request.method == 'POST':
        #product = ProductResult()
        product = Products()
        retorno = product.salvar_no_db(request.json)
        if retorno:
            return jsonify({"message": "Produto Cadastrado com Sucesso!"})
        return jsonify({"message": "Algo deu errado!"})
 
 

@api_produtos.route('/api/v1/put/produtos/<int:id_produto>', methods=['GET', 'PUT'])
@jwt_required
def put_produtos(id_produto):
    if request.method == 'PUT':
        product = Products()
        retorno = product.atualizar_no_db(request.json, id_produto)
        if retorno:
            return jsonify({"message": "Produto Atualizado com Sucesso"})
        return jsonify({"message": "Houve algum erro"})

@api_produtos.route('/api/v1/delete/produtos/<int:id_produto>', methods=['GET','DELETE'])
@jwt_required
def delete_produtos(id_produto):
    if request.method == 'DELETE':
        product = Products()
        retorno = product.remover_no_db(id_produto)
        if retorno:
            return jsonify({"message": "Produto Removido com Sucesso"})
        return jsonify({"message": "Houve algum erro"})
        
    
    
        
