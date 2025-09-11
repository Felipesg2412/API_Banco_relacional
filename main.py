#Sql_alchemy
#Permite a conexão da API com o banco de dados 
#flask permite a criação de API com python
#response e Request -> requisição
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask('carros')

#Rastear as modifcações alteradas 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

#cofiguração com o banco
# %40 -> faz o papel do @
# 1 - Usuario (root) 2- senha (Senai%40134) 3 - localhost (127.0.0.1) 4 -nome do banco
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://root:Senai%40134@127.0.0.1/db_carro'

mydb = SQLAlchemy(app)

#Classe para definir o demodelo dos dados que correspondem a tabela do banco de dados 

class Carros(mydb.Model):
    __tablename__ = 'tb_carro'
    id_carro = mydb.Column(mydb.Integer, primary_key = True)
    marca = mydb.Column(mydb.String(255))
    modelo =mydb.Column(mydb.String(255))
    ano = mydb.Column(mydb.String(255))
    cor= mydb.Column(mydb.String(255))
    valor = mydb.Column(mydb.String(255))
    numero_vendas= mydb.Column(mydb.String(255))

# Esse metodo to_json vau ser usado para converter o objeto em json 

    def to_json(self):
        return {
            "id_carro": self.id_carro,
            "marca": self.marca,
            "modelo": self.modelo,
            "ano": self.ano,
            "valor": float(self.valor),
            "cor": self.cor,
            "numero_vendas": self.numero_vendas
        }

#---------------------------------------------------
#Metodo 1- GET
@app.route('/carros', methods=['GET'])
def seleciona_carro():
    carro_selecionado = Carros.query.all()
    #Executa uma consulta no bamco de dados (Select * form tb_carros)
    carro_json=[carro.to_json()
                for carro in carro_selecionado]
    return gera_resposta(200,"carros", carro_json)

#------------------------------------------------
#Metodo 2 - GET (POR ID)
@app.route('/carros/<id_carro_pam>', methods=['GET'])
def seleciona_carro_id(id_carro_pam):
    carro_selecionado = Carros.query.filter_by(id_carro=id_carro_pam).first()
    # Select * from tb_carro where id_carro = 5
    carro_json= carro_selecionado.to_json()

    return gera_resposta(200, carro_json, 'Carro encontrado')
#-------------------------

#Metodo 3 - POST
@app.route('/carro', methods=['POST'])
def criar_carro():
    requisicao= request.get_json()

    try:
        carro= Carros(
            id_carro = requisicao['id_carro'],
            marca = requisicao['marca'],
            modelo = requisicao['modelo'],
            ano = requisicao['ano'],
            valor = requisicao['valor'],
            cor= requisicao['cor'],
            numero_vendas= requisicao['numero_vendas']
        )
        mydb.session.add(carro)
        #Adiciona ao banco 
        mydb.session.commit()
        #Salva
        return gera_resposta(201, carro.to_json(),"Criado com sucesso!")
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, {}, "Erro ao cadastrar")
#---------------------------
#Metodo 4 - DELETE
@app.route('/carros/<id_carro_pam>', methods=['DELETE'])
def deleta_carro(id_carro_pam):
    carro = Carros.query.filter_by(id_carro =id_carro_pam).first()
    try:
        mydb.session.delete(carro)
        mydb.session.commit(200,carro.to_json(), "Deletado com sucesso!")
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, {}, "Erro ao deletar!")

#------------------------------------------------
#Metodo 5 -PUT
@app.route('/carros/<id_carro_pam>', methods=['PUT'])
def atualiza_carro(id_carro_pam):
    carro= Carros.query.filter_by(id_carro=id_carro_pam).first()
    requisicao= request.get_json()

    try:
        if ('marca' in requisicao):
            carro.marca = requisicao['marca']

        if ('modelo' in requisicao):
            carro.modelo = requisicao['modelo']
        
        if ('ano' in requisicao):
            carro.ano = requisicao['ano']
        
        if ('cor' in requisicao):
            carro.cor = requisicao['cor']
        
        if ('valor' in requisicao):
            carro.valor = requisicao['valor']
        
        if ('numero_vendas' in requisicao):
            carro.numero_vendas = requisicao['numero_vendas']

        mydb.session.add(carro)
        mydb.session.commit()
        return gera_resposta(200,carro.to_json(), "Carro atualizado com sucesso")
    except Exception as e:
        print("erro", e)
        return gera_resposta(400, {}, "Erro ao atulaizar")



#Reposta padrão
    # - status (200,201)
    # nome do conteúdo
    # conteudo
    # mensagem (opcional)
def gera_resposta(status, conteudo, mensagem=False):
    body={}
    body['Lista de Carro'] = conteudo
    if (mensagem):
        body['mesagem' ]= mensagem
    return Response(json.dumps(body), status=status, mimetype='application/json')
#Dumps - Converte o dicionario criado (body) em Json (json.dumps)

app.run (port=5000, host='localhost', debug=False)