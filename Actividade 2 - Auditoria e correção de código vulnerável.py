# Sistema de gestão de menu - Código original
from flask import Flask, request, jsonify
import sqlite3
app = Flask(__name__)

# Endpoint para adicionar produto ao menu
@app.route('/api/produtos', methods=['POST'])
def adicionar_produto():
nome = request.json['nome']
preco = request.json['preco']
descricao = request.json['descricao']
categoria = request.json['categoria']
conn = sqlite3.connect('restaurante.db')
cursor = conn.cursor()
query = "INSERT INTO produtos (nome, preco, descricao, categoria) VALUES ('" + nome + "', " + str(preco) + ", '" + descricao + "', '" + categoria + "')"
cursor.execute(query)
conn.commit()
conn.close()
return jsonify({"mensagem": "Produto adicionado com sucesso!"})

# Endpoint para pesquisar produtos
@app.route('/api/produtos/pesquisa', methods=['GET'])
def pesquisar_produtos():
termo = request.args.get('termo')
conn = sqlite3.connect('restaurante.db')
cursor = conn.cursor()
query = f"SELECT * FROM produtos WHERE nome LIKE '%{termo}%' OR descricao LIKE '%{termo}%'"
cursor.execute(query)
resultados = cursor.fetchall()
conn.close()
return jsonify(resultados)

# Endpoint para atualizar preço
@app.route('/api/produtos//preco', methods=['PUT'])
def atualizar_preco(produto_id):
novo_preco = request.json['preco']
try:
conn = sqlite3.connect('restaurante.db')
cursor = conn.cursor()
cursor.execute(f"UPDATE produtos SET preco = {novo_preco} WHERE id = {produto_id}")
conn.commit()
conn.close()
return jsonify({"sucesso": True})
except Exception as e:
return jsonify({"erro": f"Erro ao atualizar: {str(e)}"}), 500

# Endpoint para login de administrador
@app.route('/api/login', methods=['POST'])
def login():
username = request.json['username']
password = request.json['password']
conn = sqlite3.connect('restaurante.db')
cursor = conn.cursor()
cursor.execute(f"SELECT * FROM usuarios WHERE username = '{username}' AND password = '{password}'")
user = cursor.fetchone()
if user:
return jsonify({"mensagem": "Login bem-sucedido!", "user_id": user[0]})
else:
return jsonify({"mensagem": "Username ou password incorretos"}), 401