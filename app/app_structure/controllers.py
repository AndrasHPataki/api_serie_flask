from .models import Products


class ProductResult():
    def __init__(self):
        self.modelo_produto = Products()
        
    def adicionar_produto(self,result):
        self.modelo_produto.name = result['name']
        self.modelo_produto.price = result['price']
        self.modelo_produto.amount = result['amount']
        return self.modelo_produto.salvar_no_db()

