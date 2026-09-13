from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)   


def conectar():
    return sqlite3.connect("../database/vagas_ti.db")


@app.route("/")
def pagina_inicial():
    return "O servidor está no ar!"


@app.route("/api/dados")
def api_dados():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT senioridade, ROUND(AVG(salario_min), 0) AS media
        FROM vagas
        GROUP BY senioridade
        ORDER BY media
    """)
    resultado_salarios = cursor.fetchall()
    salario_por_senioridade = {
        "labels": [linha[0] for linha in resultado_salarios],
        "valores": [linha[1] for linha in resultado_salarios]
    }

    cursor.execute("""
        SELECT vt.tecnologia, COUNT(*) AS qtd
        FROM vaga_tecnologia vt
        GROUP BY vt.tecnologia
        ORDER BY qtd DESC
        LIMIT 8
    """)
    resultado_tecnologias = cursor.fetchall()
    top_tecnologias = {
        "labels": [linha[0] for linha in resultado_tecnologias],
        "valores": [linha[1] for linha in resultado_tecnologias]
    }

    cursor.execute("""
        SELECT cidade, COUNT(*) AS qtd
        FROM vagas
        GROUP BY cidade
        ORDER BY qtd DESC
    """)
    resultado_cidades = cursor.fetchall()
    vagas_por_cidade = {
        "labels": [linha[0] for linha in resultado_cidades],
        "valores": [linha[1] for linha in resultado_cidades]
    }

    cursor.execute("""
        SELECT modalidade, COUNT(*) AS qtd
        FROM vagas
        GROUP BY modalidade
        ORDER BY qtd DESC
    """)
    resultado_modalidade = cursor.fetchall()
    modalidade_trabalho = {
        "labels": [linha[0] for linha in resultado_modalidade],
        "valores": [linha[1] for linha in resultado_modalidade]
    }

    cursor.execute("""
        SELECT cargo, cidade, senioridade, modalidade, salario_min, salario_max
        FROM vagas
    """)
    resultado_vagas = cursor.fetchall()
    vagas_detalhadas = [
        {
            "cargo": linha[0],
            "cidade": linha[1],
            "senioridade": linha[2],
            "modalidade": linha[3],
            "salario_min": linha[4],
            "salario_max": linha[5]
        }
        for linha in resultado_vagas
    ]

    conexao.close()

    return jsonify({
        "salario_por_senioridade": salario_por_senioridade,
        "top_tecnologias": top_tecnologias,
        "vagas_por_cidade": vagas_por_cidade,
        "modalidade_trabalho": modalidade_trabalho,
        "vagas_detalhadas": vagas_detalhadas
    })


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
