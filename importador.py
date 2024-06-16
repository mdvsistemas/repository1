import json
import sqlite3


def get_db_connection():

    conn = sqlite3.connect('base.db')
    conn.row_factory = sqlite3.Row
    return conn

produto =''
desc = ''
unidade = ''
preco = ''
imagem = ''
promo = ''
with open('produtos.json',encoding="utf-8") as produtos_json:
    listaDeprodutos = json.load(produtos_json)
    for produtos in listaDeprodutos:
        
        produto = produtos['produto']
        desc = produtos['desc']
        unidade = produtos['unidade']
        preco = format(produtos['preco'],".2f")
        imagem = produtos['imagem']
        grupo = produtos['id_grupo']
        promo = ''
        adicionais = produtos['adicionais']
        molhos = produtos['molhos']
        conn = get_db_connection()
        post = conn.execute('INSERT INTO produtos (produto,descricao,preco,unidade,preco_promo,grupo,promo,imagem,adicionais,molhos) VALUES (?,?,?,?,?,?,?,?,?,?)', 
                            (produto,desc,preco,unidade,0.00,grupo,promo,imagem,adicionais,molhos))
        conn.commit()
        conn.close()  