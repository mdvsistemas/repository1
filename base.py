from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()

class Grupo(Base):
    __tablename__ = 'grupos'
    idgrupo = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String, nullable=False)

    produtos = relationship("Produto", back_populates="grupo")

class Produto(Base):
    __tablename__ = 'produtos'
    idproduto = Column(Integer, primary_key=True, autoincrement=True)
    produto = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    idgrupo = Column(Integer, ForeignKey('grupos.idgrupo'), nullable=False)
    preco = Column(Float, nullable=False)
    unidade = Column(String, nullable=False)
    imagem = Column(String)
    ativo = Column(Integer, default=1, nullable=False)
    acompanhamento = Column(Integer, default=0, nullable=False)

    grupo = relationship("Grupo", back_populates="produtos")
    itens_carrinho = relationship("ItemCarrinho", back_populates="produto")

class Acompanhamento(Base):
    __tablename__ = 'acompanhamentos'
    idacompanhamento = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String, nullable=False)
    valoracomp = Column(Float)

    itens_acomp = relationship("ItemAcomp", back_populates="acompanhamento")

class Cliente(Base):
    __tablename__ = 'clientes'
    idcliente = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    endereco = Column(String)
    bairro = Column(String)
    ativo = Column(Integer, default=1, nullable=False)
    dtnacimento = Column(String)
    perfil = Column(Integer, default=3, nullable=False)

    carrinhos = relationship("Carrinho", back_populates="cliente")

class Carrinho(Base):
    __tablename__ = 'carrinho'
    idcarrinho = Column(Integer, primary_key=True, autoincrement=True)
    idcliente = Column(Integer, ForeignKey('clientes.idcliente'))
    dtcriacao = Column(String)
    totalcarrinho = Column(Float)

    cliente = relationship("Cliente", back_populates="carrinhos")
    itens = relationship("ItemCarrinho", back_populates="carrinho")

class ItemCarrinho(Base):
    __tablename__ = 'itenscarrinho'
    iditenscarrinho = Column(Integer, primary_key=True, autoincrement=True)
    idcarrinho = Column(Integer, ForeignKey('carrinho.idcarrinho'))
    quantidade = Column(Float, nullable=False)
    totalitem = Column(Float, nullable=False)
    idproduto = Column(Integer, ForeignKey('produtos.idproduto'))
    observacao = Column(String)

    carrinho = relationship("Carrinho", back_populates="itens")
    produto = relationship("Produto", back_populates="itens_carrinho")
    acompanhamentos = relationship("ItemAcomp", back_populates="item_carrinho")

class ItemAcomp(Base):
    __tablename__ = 'item_acomp'
    iditemcarrinho = Column(Integer, ForeignKey('itenscarrinho.iditenscarrinho'), primary_key=True)
    idacompanhamento = Column(Integer, ForeignKey('acompanhamentos.idacompanhamento'), primary_key=True)

    item_carrinho = relationship("ItemCarrinho", back_populates="acompanhamentos")
    acompanhamento = relationship("Acompanhamento", back_populates="itens_acomp")

# Conexão com o banco de dados (SQLite, por exemplo)
engine = create_engine('sqlite:///loja.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
def AdicionaCliente(nliente):
   
    session.add(nliente)
    session.commit()
    session.close()
    print("Cliente adicionado com sucesso!")

'''# Criar uma sessão
Session = sessionmaker(bind=engine)
session = Session()

# Inserir dados
# Criar grupos
grupo1 = Grupo(descricao="Grupo 1")
grupo2 = Grupo(descricao="Grupo 2")
session.add(grupo1)
session.add(grupo2)
session.commit()

# Criar produtos
produto1 = Produto(produto="Produto 1", descricao="Descrição do Produto 1", idgrupo=grupo1.idgrupo, preco=10.0, unidade="un")
produto2 = Produto(produto="Produto 2", descricao="Descrição do Produto 2", idgrupo=grupo1.idgrupo, preco=15.0, unidade="un")
produto3 = Produto(produto="Produto 3", descricao="Descrição do Produto 3", idgrupo=grupo2.idgrupo, preco=20.0, unidade="un")
produto4 = Produto(produto="Produto 4", descricao="Descrição do Produto 4", idgrupo=grupo2.idgrupo, preco=25.0, unidade="un")
session.add(produto1)
session.add(produto2)
session.add(produto3)
session.add(produto4)
session.commit()

# Criar clientes
cliente1 = Cliente(nome="Cliente 1", telefone="123456789", email="cliente1@example.com")
cliente2 = Cliente(nome="Cliente 2", telefone="987654321", email="cliente2@example.com")
session.add(cliente1)
session.add(cliente2)
session.commit()

# Criar carrinho para cliente1
carrinho1 = Carrinho(idcliente=cliente1.idcliente, dtcriacao="2024-06-18", totalcarrinho=0.0)
session.add(carrinho1)
session.commit()

# Adicionar itens ao carrinho
item1 = ItemCarrinho(idcarrinho=carrinho1.idcarrinho, quantidade=2, totalitem=produto1.preco * 2, idproduto=produto1.idproduto, observacao="Sem observação")
item2 = ItemCarrinho(idcarrinho=carrinho1.idcarrinho, quantidade=1, totalitem=produto3.preco, idproduto=produto3.idproduto, observacao="Sem observação")
session.add(item1)
session.add(item2)
session.commit()

# Atualizar total do carrinho
carrinho1.totalcarrinho = item1.totalitem + item2.totalitem
session.commit()

# Fechar a sessão
session.close()
'''
