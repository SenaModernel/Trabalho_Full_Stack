from flask import Flask, make_response, jsonify, request
import mysql.connector

# Configurações da conexão
conexao = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='atitus_bd',  # Substitua pelo nome do seu banco de dados
    user='Pedro Sena',      # Substitua pelo seu usuário
    password='Luciane20.'   # Substitua pela sua senha
)

if conexao.is_connected():
    print('Conectado ao banco de dados com sucesso!')

cursor = conexao.cursor()  # Cria um cursor

app = Flask("Gerenciador de Produtos")

# Função para buscar produtos
def obter_produtos():
    cursor.execute("SELECT * FROM list_produto")  # Executa a consulta
    produtos = cursor.fetchall()  # Busca todos os registros
    columns = [column[0] for column in cursor.description]  # Obtém os nomes das colunas
    resultado = [dict(zip(columns, produto)) for produto in produtos]  # Transforma em dicionários
    return resultado

@app.route('/produtos', methods=['GET'])
def get_produtos():
    produtos = obter_produtos()  # Chama a função para obter produtos
    return make_response(jsonify(produtos), 200)  # Retorna os produtos em formato JSON

# Endpoint para pegar um produto e reduzir a quantidade
@app.route('/produtos/<int:id_produto>/pegar', methods=['POST'])
def pegar_produto(id_produto):
    try:
        # Verifica se o produto existe e qual sua quantidade
        cursor.execute("SELECT Quant_estoq FROM list_produto WHERE id_Prod = %s", (id_produto,))
        resultado = cursor.fetchone()

        if resultado is None:
            return make_response(jsonify({"error": "Produto não encontrado"}), 404)  # Produto não existe

        quantidade_atual = resultado[0]

        if quantidade_atual > 0:
            nova_quantidade = quantidade_atual - 1  # Subtrai 1 do estoque
            cursor.execute("UPDATE list_produto SET Quant_estoq = %s WHERE id_Prod = %s", (nova_quantidade, id_produto))
            conexao.commit()  # Confirma a operação no banco
            return make_response(jsonify({"message": "Produto retirado com sucesso", "nova_quantidade": nova_quantidade}), 200)
        else:
            return make_response(jsonify({"error": "Estoque insuficiente"}), 400)

    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

if __name__ == '__main__':
    app.run(debug=True)  # Inicia o servidor Flask
