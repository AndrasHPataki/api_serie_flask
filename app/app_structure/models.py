from . import db, ma

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25))
    password = db.Column(db.String(100))

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25),nullable=False)
    price = db.Column(db.Integer,nullable=False)
    amount = db.Column(db.Integer,nullable=False)
    
   
        
    def salvar_no_db(self,result):
    
        self.name = result['name']
        self.price = result['price']
        self.amount = result['amount']
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False
        
        
    def atualizar_no_db(self,arg1, arg2):
        try:
            db.session.query(self).filter(Product.id==arg2).update(arg1)
            db.session.commit()
            return True
        except:
            return False
    
    def remover_no_db(self,arg1):
        try:
            Products.query.filter(Products.id==arg1).delete()
            #db.session.query(self).filter(self.id==arg1).delete()
            db.session.commit()
            return True
        except:
            return False
      
            
        
    

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('amount','id', 'name', 'price')

class TokenBlacklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(3000))

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password')

one_user_schema = UserSchema()
many_users_schema = UserSchema(many=True)
#VARIAVEIS PARA SERIALIZAR PRODUCTS
one_product_schema = ProductSchema()
many_products_schema = ProductSchema(many=True)
