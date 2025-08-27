from flask import Flask, jsonify, request
app = Flask(__name__)


usuarios = []

@app.route('/users', methods=['POST'])
def createUsers():
    dados = request.get_json()
    nome = dados.get("nome")
    email = dados.get("email")

    newUser = {'nome': nome, 'email': email, 'id': len(usuarios)+1}
    usuarios.append(newUser)


    return jsonify(newUser), 201

@app.route('/users', methods=['GET'])
def getUsers():
    return jsonify(usuarios), 200


@app.route('/users/<int:id>', methods=['GET'])
def getUniqueUser(id):
    for user in usuarios:
        if user['id'] == id:
            return jsonify(user)
    
    return jsonify({"Error404": "Not Found!"}), 404


@app.route('/users/<int:id>', methods=['PUT'])
def updateUser(id):
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
    for i, user in enumerate(usuarios):
        if user['id'] == id:
            usuarios.remove(user)
            return jsonify({"mensagem": "Usuario excluido com sucesso!"}), 200
    
    return jsonify({"Error404": "Not Found!"}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5000)