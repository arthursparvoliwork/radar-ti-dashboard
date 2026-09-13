from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "vagas_ti.db")

def conectar():
    return sqlite3.connect(DB_PATH)

@app.route("/")
def pagina_inicial():
    return "O servidor está no ar!"

@app.route("/api/dados")
def api_dados():
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT senioridade, ROUND(AVG(salario_min), 0) AS media
            FROM vagas GROUP BY senioridade ORDER BY media
        """)
        resultado_salarios = cursor.fetchall()
        salario_por_senioridade = {
            "labels": [l[0] for l in resultado_salarios],
            "valores": [l[1] for l in resultado_salarios]
        }

        cursor.execute("""
            SELECT vt.tecnologia, COUNT(*) AS qtd
            FROM vaga_tecnologia vt
            GROUP BY vt.tecnologia ORDER BY qtd DESC LIMIT 8
        """)
        top_tecnologias = {"labels": [], "valores": []}
        for l in cursor.fetchall():
            top_tecnologias["labels"].append(l[0])
            top_tecnologias["valores"].append(l[1])

        cursor.execute("""
            SELECT cidade, COUNT(*) AS qtd
            FROM vagas GROUP BY cidade ORDER BY qtd DESC
        """)
        vagas_por_cidade = {"labels": [], "valores": []}
        for l in cursor.fetchall():
            vagas_por_cidade["labels"].append(l[0])
            vagas_por_cidade["valores"].append(l[1])

        cursor.execute("""
            SELECT modalidade, COUNT(*) AS qtd
            FROM vagas GROUP BY modalidade ORDER BY qtd DESC
        """)
        modalidade_trabalho = {"labels": [], "valores": []}
        for l in cursor.fetchall():
            modalidade_trabalho["labels"].append(l[0])
            modalidade_trabalho["valores"].append(l[1])

        cursor.execute("""
            SELECT cargo, cidade, senioridade, modalidade, salario_min, salario_max
            FROM vagas
        """)
        vagas_detalhadas = [
            {"cargo": l[0], "cidade": l[1], "senioridade": l[2],
             "modalidade": l[3], "salario_min": l[4], "salario_max": l[5]}
            for l in cursor.fetchall()
        ]

        conexao.close()
        return jsonify({
            "salario_por_senioridade": salario_por_senioridade,
            "top_tecnologias": top_tecnologias,
            "vagas_por_cidade": vagas_por_cidade,
            "modalidade_trabalho": modalidade_trabalho,
            "vagas_detalhadas": vagas_detalhadas
        })
    except Exception as e:
        return
