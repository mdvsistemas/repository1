# _*_ coding: utf-8 _*_
from flask import Flask,render_template, url_for,redirect,request,session,flash
import sqlite3
import datetime


app = Flask(__name__)
app.config['SECRET_KEY']='marcio'

def get_db_connection():

    conn = sqlite3.connect('base.db')
    conn.row_factory = sqlite3.Row
    return conn
def grupo_cliente():
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM clientes WHERE telefone =?',
                        (session['clienteLogado'],) ).fetchone()
    conn.close()
    grupo = post['grupo']
    return grupo
@app.route('/')
def home():
    if 'clienteLogado' in session:
        conn = get_db_connection()
        post = conn.execute('SELECT * FROM clientes WHERE telefone = ?',
                        (session['clienteLogado'],) ).fetchone()
        conn.close()
        nome = 'Ola, seja bem vindo '+post['nome']
        grupo = post['grupo']
        
    else:
        nome = 'Para continuar, efetue o login'
        grupo =''
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM produtos where ativo = 1',).fetchall()
    conn.close()
    

    listaDeprodutos =post
    return render_template('home.html',nome=nome,grupo=grupo,produtos=listaDeprodutos)

@app.route('/<categoria>')
def home1(categoria):
    
    if categoria== "favicon.ico":
        
        return redirect('/')
    if 'clienteLogado' in session:
        conn = get_db_connection()
        post = conn.execute('SELECT * FROM clientes WHERE telefone = ?',
                        (session['clienteLogado'],) ).fetchone()
        conn.close()
        nome = 'Ola, seja bem vindo '+post['nome']
        grupo = post['grupo']
        
    else:
        nome = 'Para continuar, efetue o login'
        grupo =''
    if categoria=='':
        conn = get_db_connection()
        post = conn.execute('SELECT * FROM produtos where ativo =1').fetchall()
        conn.close()
    else:
        conn = get_db_connection()
        post = conn.execute('SELECT * FROM produtos where ativo =1 and grupo =?',categoria,).fetchall()
        conn.close()

    listaDeprodutos =post
    return render_template('home.html',nome=nome,grupo=grupo,produtos=listaDeprodutos,)

@app.route('/admin')
def admin():
    consulta =''
    consulta = 'SELECT clientes.nome AS nome,clientes.endereco AS endereco ,clientes.telefone AS telefone, carrinho.fechado AS status, round(SUM(itens_carrinho.valor_unit*itens_carrinho.quantidade),2) AS total_carrinho'
    consulta = consulta+' ,carrinho.idcarrinho as idcarrinho FROM clientes JOIN carrinho ON clientes.idcliente = carrinho.idcliente AND carrinho.fechado=1 JOIN itens_carrinho ON carrinho.idcarrinho = itens_carrinho.idcarrinho WHERE '
    consulta= consulta +'clientes.idcliente = carrinho.idcliente GROUP BY clientes.nome, carrinho.idcarrinho,carrinho.fechado;'
    
    conn = get_db_connection()
    pedidos = conn.execute(consulta, ).fetchall()
    conn.close()
    
    conn = get_db_connection()
    return render_template('admin.html',pedidos=pedidos,)

@app.route('/login')
def login():
    return render_template('loginCliente.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/logout')
def logout():
    
    del session['clienteLogado']
    return redirect('/')

@app.route('/perfil')
def perfil():
    if 'clienteLogado' in session:
        conn = get_db_connection()
        post = conn.execute('SELECT * FROM clientes WHERE telefone = ?',
                        (session['clienteLogado'],) ).fetchone()
        conn.close()
        carrinho=lista_carrinho(post['idcliente'])
        st=0
        for item in carrinho:
            st = st+item['Sub_total']
        return render_template('cliente.html',nome=post['nome'], email=post['email'], telefone=post['telefone'],
                carrinho=carrinho,subtotal=round(st,2))
    else:
        flash('Primeiro efetue seu login!')
        return redirect('/login')
    
def lista_carrinho(idcliente):
    conn = get_db_connection()
    carrinho = conn.execute('SELECT p.produto, i.quantidade,i.valor_unit,(i.valor_unit*i.quantidade) as Sub_total,p.imagem,i.iditemcarrinho,i.observacoes,i.idcarrinho FROM itens_carrinho as i,produtos as p WHERE i.idcarrinho in (SELECT idcarrinho from carrinho where idcliente =? and fechado =0)  and p.idproduto=i.idproduto',
                        (idcliente,) ).fetchall()
    conn.close()
    
    return carrinho

@app.route('/altera_item/<operador>/<item>')
def altera_item(item,operador):
    print(f' operador {operador} e item {item}')
    if operador=="menos":
        conn = get_db_connection()
        post = conn.execute('UPDATE itens_carrinho SET quantidade=quantidade-1 WHERE iditemcarrinho=?',(item,))
        conn.commit()
        conn.close()
    elif operador=="mais":
        conn = get_db_connection()
        post = conn.execute('UPDATE itens_carrinho SET quantidade=quantidade+1 WHERE iditemcarrinho=?',(item,))
        conn.commit()
        conn.close()
    conn = get_db_connection()
    carrinho = conn.execute('SELECT * from itens_carrinho WHERE iditemcarrinho=?',(item,)).fetchone()
    conn.close()
    if carrinho['quantidade']<=0:
        conn = get_db_connection()
        post = conn.execute('DELETE FROM itens_carrinho WHERE iditemcarrinho=?',(item,))
        conn.commit()
        conn.close()
    return redirect('/perfil')
@app.route('/novasenha',methods=['POST'])
def novasenha():
    senhad = request.form.get('novaSenha') 
    if 'clienteLogado' in session:
        conn = get_db_connection()
        post = conn.execute('SELECT * FROM clientes WHERE telefone = ?',
                        (session['clienteLogado'],) ).fetchone()
        conn.close()
        
        conn = get_db_connection()
        post = conn.execute('UPDATE clientes SET senha = ? WHERE telefone=?',(senhad,session['clienteLogado']))
        conn.commit()
        conn.close()  
        return redirect('/perfil')
    else:
        flash('Primeiro efetue seu login!')
        return redirect('/login')
    
    
@app.route('/acesso_cliente',methods=['POST'])
def acesso():
    telefoned = request.form.get('telefone') 
    senhad = request.form.get('senha') 
    #---- localiza o cliente --------------------
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM clientes WHERE telefone = ?',
                        (telefoned,) ).fetchone()
    conn.close()

    if post is None:
        flash('Usuário inexistente')  
        return redirect('/login')
       
    elif post['telefone'] != telefoned or post['senha'] != senhad:
        flash('Usuário ou senha não conferem')  
        return redirect('/login')
    else:
        
        session['clienteLogado']=post['telefone']
        return redirect('/perfil') 
    
@app.route('/incluir_carrinho', methods=['POST'])
def incluir_carr():
    #idcliente = session['clienteLogado']
    idproduto = request.form.get('idproduto')
    valor_unit = request.form.get('preco')
    quantidade = float(request.form.get('quantidade'))
    adicionais = request.form.get('adicionais')
    print(f'quantidade {quantidade}')
    if quantidade == 0:
        return redirect("/perfil")

    #----- localiza o cliente pelo telefone -----
    conn = get_db_connection()
    cli = conn.execute('SELECT idcliente FROM clientes WHERE telefone = ?', (session['clienteLogado'],) ).fetchone()
    conn.close()
    id_cli = cli['idcliente']
    #-----verifica se tem carrinho em aberto -----
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM carrinho WHERE idcliente = ? and fechado = 0',
                        (id_cli,) ).fetchone()
    conn.close() 
    
    if post is None:
        conn = get_db_connection()
        carrinho = conn.execute('INSERT INTO carrinho (idcliente,fechado) VALUES (?,0)',(id_cli,))
        conn.commit()
        conn.close()
        
    
    #---- inclui item no carrinho -----   
    conn = get_db_connection()
    carrinho = conn.execute('SELECT * FROM carrinho WHERE idcliente = ? and fechado = 0',
                    (id_cli,) ).fetchone()
    conn.close() 
    
    #verifica se o item ja exista no carrinho
    conn = get_db_connection()
    jaexiste = conn.execute('SELECT idproduto FROM itens_carrinho WHERE idcarrinho = ? and idproduto=?',
                    (carrinho['idcarrinho'],idproduto,) ).fetchone()
    print('chegou aqui')
    conn.close() 
    if jaexiste is None:
        conn = get_db_connection()
        item_carrinho = conn.execute('INSERT INTO itens_carrinho (idcarrinho,quantidade,valor_unit,idproduto,observacoes) VALUES (?,?,?,?,?)',
                                    (carrinho['idcarrinho'],round(quantidade,2),valor_unit,idproduto,adicionais))
        conn.commit()
        conn.close() 
        print('item incluido')
    else:
        conn = get_db_connection()
        item_carrinho = conn.execute('UPDATE itens_carrinho SET quantidade=quantidade+?,observacoes=? WHERE idproduto=?',(round(quantidade,2),adicionais,idproduto))
        conn.commit()
        conn.close()
        print('item ja existia')

    return redirect("/perfil")

@app.route('/cadastro_cliente',methods=['POST'])
def cad_cli():
    nome =  request.form.get('nome')
    email =  request.form.get('email')
    telefone = request.form.get('telefone') 
    endereco = request.form.get('endereco') 
    bairro = request.form.get('bairro') 
    senha = request.form.get('senhaCliente') 
    #---- validar se client existe ---
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM clientes WHERE telefone = ?',
                        (telefone,) ).fetchone()
    conn.close()
    if post is None:
        conn = get_db_connection()
        post = conn.execute('INSERT INTO clientes (nome,email,telefone,senha,endereco,bairro,grupo) VALUES (?,?,?,?,?,?,?)',(nome,email,telefone,senha,endereco,bairro,3))
        conn.commit()
        conn.close()  
        return redirect('/login')
    else:
        flash('Usuário ja existe')
        return redirect('/cadastro')

@app.route('/produto/<id>')
def produto(id :str):
    if 'clienteLogado' in session:
        conn = get_db_connection()
        post = conn.execute('SELECT * FROM clientes WHERE telefone = ?',
                        (session['clienteLogado'],) ).fetchone()
        conn.close()
        
    else:
        flash('Primeiro efetue seu login!')
        return redirect('/login')
    
    

    conn = get_db_connection()
    post = conn.execute('SELECT * FROM produtos WHERE ativo =1 and idproduto = ?',(id,)).fetchone()
    conn.close()
    
    if post is None :
        return render_template('produto.html',id=id, produto=" Produto não localizado", desc="", unidade="", preco="",imagem="")
    else:
        return render_template('produto.html',id=post['idproduto'], produto=post['produto'], desc=post['descricao'], unidade=post['unidade'], preco=post['preco'],imagem=post['imagem'],promo=post['promo'],
                               adicionais=post['adicionais'],molhos=post['molhos'],  )     

@app.route('/finaliza_carrinho')
def finaliza_carrinho():
    if 'clienteLogado' in session:
        conn = get_db_connection()
        post = conn.execute('SELECT * FROM clientes WHERE telefone = ?',
                        (session['clienteLogado'],) ).fetchone()
        conn.close()
        
        carrinho=lista_carrinho(post['idcliente'])
        st=0
        for item in carrinho:
            st = st+item['Sub_total']
    return render_template('finalizar_carrinho.html',idcliente=post['idcliente'],nome=post['nome'], email=post['email'], telefone=post['telefone'],carrinho=carrinho,subtotal=round(float(st),2))
@app.route('/envia/<idcliente>')
def whats(idcliente):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM clientes WHERE idcliente = ?',
                    (idcliente,) ).fetchone()
    conn.close()
    print(f'id carrinho  e cliente {idcliente}')
        
    carrinho=lista_carrinho(idcliente)
    st=0
    agora = datetime.datetime.now()
    
    agora_string = agora.strftime("%d/%m/%Y %H:%M")
   
    with open(f"./static/pedidos/cliente_{post['telefone']}.txt", "w") as arquivo:
	    arquivo.write(f"Pedido do cliente {post['nome']} \ntelefone {post['telefone']} \nemail {post['email']} \n gerado as {agora_string} \n")
    
    for item in carrinho:
        st = st+item['Sub_total']
        idcarrinho = item['idcarrinho']
        with open(f"./static/pedidos/cliente_{post['telefone']}.txt", "a") as arquivo:
            arquivo.write(f"\nitem: {item[0]} Qtd: {item[1]} valor: {item[3]} observacao: {item[6]}")
    
    with open(f"./static/pedidos/cliente_{post['telefone']}.txt", "a") as arquivo:
            arquivo.write(f"\n\nValor total: R$ {round(st,2)} ")
   
    conn = get_db_connection()
    carrinho = conn.execute('update carrinho set fechado = 1 where idcarrinho =?',(idcarrinho,
                         )).fetchall()
  
    conn.commit()
    conn.close()
    return redirect('/') 

@app.route('/altprd/<id>',methods=['POST','GET'])
def alterar_prd(id:str):
    print(f'grupo cliente {grupo_cliente()}')
    if grupo_cliente() !=1:
        return redirect('/perfil')
    
    conn = get_db_connection()
    lproduto = conn.execute('SELECT * FROM produtos where idproduto=?',(id,)).fetchone()
    conn.close()
    conn = get_db_connection()
    categoria = conn.execute('SELECT * FROM grupo ').fetchall()
    conn.close()
    return render_template('altera_produto.html',produto=lproduto,categoria=categoria)


@app.route('/edpr/<id>',methods=['POST','GET'])
def edpr(id:str):
    
    if 'clienteLogado' in session:
        conn = get_db_connection()
        post = conn.execute('SELECT * FROM clientes WHERE telefone = ?',
                        (session['clienteLogado'],) ).fetchone()
        conn.close()
        
        if post['grupo'] !=1:
            return redirect('/perfil')    
    if id=="0":
        
        conn = get_db_connection()
        lprodutos = conn.execute('SELECT * FROM produtos').fetchall()
        conn.close()
    elif id=="where": 
        query =  request.form.get('pesquisa') 
        consulta =f'SELECT * FROM produtos WHERE descricao like "%{query}%" or produto like "%{query}%" '
        
        conn = get_db_connection()
        lprodutos = conn.execute(consulta).fetchall()
        conn.close()
    else:
        
        conn = get_db_connection()
        lprodutos = conn.execute('SELECT * FROM produtos where idproduto=?',(id,)).fetchall()
        conn.close()
    
    if lprodutos is not None: 
        return render_template('editp.html',produtos=lprodutos,) 
    else:
        return redirect('/edpr/*')
      
@app.route('/atualiza_produto',methods=['POST'])
def atualiza_produto():
    idproduto = request.form.get('idproduto')
    produto = request.form.get('nomproduto')
    descricao = request.form.get('descproduto')
    unidade = request.form.get('unidproduto')
    preco = request.form.get('precoproduto')
    
    adicionais = request.form.get('adicionais')
    molhos = request.form.get('molhos')
    categoria = request.form.get('categoria')
    ativo = request.form.get('ativo')
    print(f'ativo {ativo}')
    if ativo is None: 
        ativo = 0
    conn = get_db_connection()  
    post = conn.execute('UPDATE produtos SET produto=?,descricao=?,unidade=?,preco=?,adicionais=?,molhos=?,grupo=?,ativo=? WHERE idproduto=?',(produto,descricao,unidade,preco,adicionais,molhos,categoria,ativo,idproduto))
    conn.commit()   
    conn.close()
    return redirect('/edpr/0')

@app.route('/baixa/<idcarr>')
def baixa(idcarr):
    conn = get_db_connection()
    post = conn.execute('UPDATE carrinho set fechado =-1 WHERE idcarrinho = ?',
                    (idcarr,) ).fetchone()
    conn.commit()
    conn.close()
    return redirect('/admin')
                 
if __name__ in '__main__':
    app.run(debug=True, host='0.0.0.0', port=50000) 