from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True)
    nome = Column(String)

    # Um cliente pode ter vários carrinhos
    carrinhos = relationship("CarrinhoCompras", back_populates="cliente")

class Produto(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    preco = Column(Float)

    # Um produto pode estar em vários itens de carrinho
    itens_carrinho = relationship("ItensCarrinho", back_populates="produto")

class CarrinhoCompras(Base):
    __tablename__ = 'carrinho_compras'
    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))

    # Relacionamento com cliente
    cliente = relationship("Cliente", back_populates="carrinhos")

    # Um carrinho pode ter vários itens
    itens = relationship("ItensCarrinho", back_populates="carrinho")

class ItensCarrinho(Base):
    __tablename__ = 'itens_carrinho'
    id = Column(Integer, primary_key=True)
    carrinho_id = Column(Integer, ForeignKey('carrinho_compras.id'))
    produto_id = Column(Integer, ForeignKey('produtos.id'))
    quantidade = Column(Integer)

    # Relacionamentos
    carrinho = relationship("CarrinhoCompras", back_populates="itens")
    produto = relationship("Produto", back_populates="itens_carrinho")

# Conexão com o banco de dados (SQLite, por exemplo)
engine = create_engine('sqlite:///loja.db')
Base.metadata.create_all(engine)

# Criar uma sessão
Session = sessionmaker(bind=engine)
session = Session()

# Adicionar alguns dados de exemplo
cliente = Cliente(nome="João Silva")
produto1 = Produto(nome="Produto A", preco=10.0)
produto2 = Produto(nome="Produto B", preco=20.0)
carrinho = CarrinhoCompras(cliente=cliente)
item1 = ItensCarrinho(carrinho=carrinho, produto=produto1, quantidade=2)
item2 = ItensCarrinho(carrinho=carrinho, produto=produto2, quantidade=1)

# Salvar no banco de dados
session.add(cliente)
session.add(produto1)
session.add(produto2)
session.add(carrinho)
session.add(item1)
session.add(item2)
session.commit()

# Consulta para retornar o carrinho com os produtos comprados por um cliente
def obter_carrinho_cliente(cliente_id):
    carrinho = session.query(CarrinhoCompras).filter(CarrinhoCompras.cliente_id == cliente_id).first()
    if carrinho:
        print(f"Carrinho ID: {carrinho.id}")
        for item in carrinho.itens:
            produto = item.produto
            print(f"Produto: {produto.nome}, Preço: {produto.preco}, Quantidade: {item.quantidade}")
    else:
        print("Carrinho não encontrado para este cliente.")

# Exemplo de uso
obter_carrinho_cliente(cliente.id)

# Fechar a sessão
session.close()
