from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)


usuarios = []

@app.route('/users', methods=['POST'])
def createUsers():
    """
    Cria um novo usuário
    ---
    tags:
    - Usuários
    description: Cria um novo usuário com nome e e-mail.
    consumes:
    - application/json
    produces:
    - application/json
    parameters:
    - in: body
      name: user
      description: Objeto JSON com os dados do usuário
      required: true
      schema:
        type: object
        required:
          - nome
          - email
        properties:
          nome:
            type: string
            example: Yuri Gonçalves
          email:
            type: string
            example: yuri@email.com
    responses:
      201:
        description: Usuário criado com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            nome:
              type: string
              example: Yuri Gonçalves
            email:
              type: string
              example: yuri@email.com
      400:
        description: Requisição inválida, verifique o nome ou o e-mail
        schema:
          type: object
    """
    dados = request.get_json()
    nome = dados.get("nome")
    email = dados.get("email")

    newUser = {'nome': nome, 'email': email, 'id': len(usuarios)+1}
    usuarios.append(newUser)


    return jsonify(newUser), 201

@app.route('/users', methods=['GET'])
def getUsers():
    """
    Lista todos os usuários
    ---
    tags:
    - Usuários
    description: Retorna uma lista de todos os usuários cadastrados.
    produces:
    - application/json
    responses:
      200:
        description: Lista de usuários retornada com sucesso
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              nome:
                type: string
                example: Yuri Gonçalves
              email:
                type: string
                example: yuri@email.com
    """
    return jsonify(usuarios), 200


@app.route('/users/<int:id>', methods=['GET'])
def getUniqueUser(id):
    """
    Busca um usuário específico
    ---
    tags:
    - Usuários
    description: Retorna os dados de um usuário a partir do seu ID.
    produces:
    - application/json
    parameters:
    - name: id
      in: path
      type: integer
      required: true
      description: ID do usuário
      example: 1
    responses:
      200:
        description: Usuário encontrado com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            nome:
              type: string
              example: Yuri Gonçalves
            email:
              type: string
              example: yuri@email.com
      404:
        description: Usuário não encontrado
        schema:
          type: object
    """
    for user in usuarios:
        if user['id'] == id:
            return jsonify(user)
    
    return jsonify({"Error404": "Not Found!"}), 404


@app.route('/users/<int:id>', methods=['PUT'])
def updateUser(id):
    """
    Atualiza um usuário existente
    ---
    tags:
    - Usuários
    description: Atualiza os dados (nome e e-mail) de um usuário a partir do seu ID.
    consumes:
    - application/json
    produces:
    - application/json
    parameters:
    - name: id
      in: path
      type: integer
      required: true
      description: ID do usuário
      example: 1
    - in: body
      name: user
      description: Objeto JSON com os novos dados do usuário
      required: true
      schema:
        type: object
        required:
          - nome
          - email
        properties:
          nome:
            type: string
            example: Yuri Gabriel
          email:
            type: string
            example: yuri@email.com
    responses:
      200:
        description: Usuário atualizado com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            nome:
              type: string
              example: Yuri Gabriel
            email:
              type: string
              example: yuri@email.com
      404:
        description: Usuário não encontrado
        schema:
          type: object
    """


    for i, user in enumerate(usuarios):
        if user['id'] == id:
            dados = request.get_json()
            nome = dados.get("nome")
            email = dados.get("email")
            userUpdated = {'nome': nome, 'email': email, 'id': id}

            usuarios[i] = userUpdated

            return jsonify(userUpdated), 200
    
    return jsonify({"Error404": "Not Found!"}), 404


@app.route('/users/<int:id>', methods=['DELETE'])
def deleteUser(id):
    """
    Exclui um usuário existente
    ---
    tags:
    - Usuários
    description: Exclui um usuário a partir do seu ID.
    produces:
    - application/json
    parameters:
    - name: id
      in: path
      type: integer
      required: true
      description: ID do usuário a ser excluído
      example: 1
    responses:
      200:
        description: Usuário excluído com sucesso
        schema:
          type: object
          properties:
            mensagem:
              type: string
              example: "Usuario excluido com sucesso!"
      404:
        description: Usuário não encontrado
        schema:
          type: object
    """
    
    for i, user in enumerate(usuarios):
        if user['id'] == id:
            usuarios.remove(user)
            return jsonify({"mensagem": "Usuario excluido com sucesso!"}), 200
    
    return jsonify({"Error404": "Not Found!"}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5001)