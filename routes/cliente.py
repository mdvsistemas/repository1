from flask import Blueprint, render_template,request
from database.cliente import CLIENTES

cliente_route = Blueprint('cliente',__name__)

@cliente_route.route('/')
def lista_clientes():
    return render_template('lista_clientes.html', clientes = CLIENTES)

@cliente_route.route('/', methods = ['POST'])
def inserir_clientes():
    data= request.json
    novo_usuario ={
        "id":len(CLIENTES)+1,
        "nome": data['nome'],
        "email": data['email'],
        "telefone": data['telefone']
    }
    CLIENTES.append(novo_usuario)
    return render_template('item_cliente.html',cliente = novo_usuario)

@cliente_route.route('/new')
def form_clientes():
    return render_template('form_clientes.html')

@cliente_route.route('/<int:cliente_id>')
def detalhe_cliente(cliente_id):
    return render_template('detalhe_cliente.html')

@cliente_route.route('/<int:cliente_id>/edit')
def form_edit_cliente(cliente_id):
    return render_template('form_edit_cliente.html')

@cliente_route.route('/<int:cliente_id>/update', methods = ['PUT'])
def atualizar_cliente():
    pass  

@cliente_route.route('/<int:cliente_id>/delete', methods = ['PUT'])
def deletar_cliente():
    pass


