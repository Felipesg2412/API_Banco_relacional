# Atividade Banco Relacional veterinária

from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask('pet') # É uma boa prática usar __name__ aqui
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Senai%40134@127.0.0.1/db_vet'

dbvet = SQLAlchemy(app)

class Cliente(dbvet.Model):
    __tablename__ = 'tb_clientes'
    id_cliente = dbvet.Column(dbvet.Integer, primary_key=True)
    nome = dbvet.Column(dbvet.String(255))

class Pet(dbvet.Model):
    __tablename__ = 'tb_pets'
    id_pet = dbvet.Column(dbvet.Integer, primary_key=True)
    nome = dbvet.Column(dbvet.String(255))
    tipo = dbvet.Column(dbvet.String(255))
    raca = dbvet.Column(dbvet.String(255))
    idade = dbvet.Column(dbvet.String(255)) 
    data_nascimento = dbvet.Column(dbvet.String(255))
    id_clienteF = dbvet.Column(dbvet.Integer, dbvet.ForeignKey('tb_clientes.id_cliente'), nullable=False)

    def to_json(self):
        return {
            'id_pet': self.id_pet,
            'nome': self.nome,
            'tipo': self.tipo,
            'raca': self.raca,
            'idade': self.idade,
            'data_nascimento': str(self.data_nascimento),
            # .isoformat() if self.data_nascimento else None,
            'id_cliente': self.id_clienteF, # O dono do pet
        }

# RESPOSTA PADRÃO
def gera_resposta(status, conteudo, mensagem=False):
    body = {}
    body['dados'] = conteudo
    if (mensagem):
        body['mensagem'] = mensagem
    return Response(json.dumps(body), status=status, mimetype='application/json')

# --- ROTAS DA API PARA PETS ---

# GET (Todos os pets)
@app.route('/pet', methods=['GET'])
def seleciona_pets():
    pets_selecionados = Pet.query.all()
    pets_json = [pet.to_json() for pet in pets_selecionados]
    return gera_resposta(200, pets_json, "Lista de pets")

# GET (Pet por ID)
@app.route('/pet/<id_pet>', methods=['GET'])
def seleciona_pet_por_id(id_pet):
    pet_selecionado = Pet.query.filter_by(id_pet=id_pet).first()

    if not pet_selecionado:
        return gera_resposta(404, {}, "Pet não encontrado")

    pet_json = pet_selecionado.to_json()
    return gera_resposta(200, pet_json, 'Pet encontrado')

# POST (Criar novo pet)
@app.route('/pet', methods=['POST'])
def novo_pet():
    requisicao = request.get_json()
    try:
        # Usando o modelo 'Pet'
        pet = Pet(
            id_pet = requisicao['id_pet'],
            nome = requisicao['nome'],
            tipo = requisicao['tipo'],
            raca = requisicao['raca'],
            data_nascimento = requisicao['data_nascimento'],
            id_clienteF = requisicao['id_cliente'],
            idade = requisicao['idade']
        )
        dbvet.session.add(pet)
        dbvet.session.commit()
        return gera_resposta(201, pet.to_json(), 'Pet criado com Sucesso')
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, {}, "Erro ao cadastrar pet!")

# DELETE (Deletar um pet)
@app.route('/pet/<id_pet>', methods=['DELETE'])
def deleta_pet(id_pet):
    pet = Pet.query.filter_by(id_pet=id_pet).first()

    if not pet:
        return gera_resposta(404, {}, "Pet não encontrado")

    try:
        dbvet.session.delete(pet)
        dbvet.session.commit()
        return gera_resposta(200, pet.to_json(), 'Pet deletado com Sucesso')
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, {}, "Erro ao deletar pet")

# PUT (Atualizar um pet)
@app.route("/pet/<id_pet>", methods=['PUT'])
def atualiza_pet(id_pet):
    pet = Pet.query.filter_by(id_pet=id_pet).first()
    
    if not pet:
        return gera_resposta(404, {}, "Pet não encontrado")

    requisicao = request.get_json()

    try:
        if ('nome' in requisicao):
            pet.nome = requisicao['nome']
        if ('tipo' in requisicao):
            pet.tipo = requisicao['tipo']
        if ('raca' in requisicao):
            pet.raca = requisicao['raca']
        if ('idade' in requisicao):
            pet.idade = requisicao['idade']
        if ('data_nascimento' in requisicao):
            pet.data_nascimento = requisicao['data_nascimento']
        if ('id_cliente' in requisicao):
            pet.id_clienteF = requisicao['id_cliente']

        dbvet.session.add(pet)
        dbvet.session.commit()
        return gera_resposta(200, pet.to_json(), 'Pet atualizado com Sucesso')
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, {}, "Erro ao atualizar pet")

if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)