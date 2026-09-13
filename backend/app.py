from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DB_PATH = os.path.join("/app", "database", "vagas_ti.db")

def conectar():
    return sqlite3.connect(DB_PATH)

@app.route("/")
def pagina_inicial():
    return "O servidor está no ar!"

@app.route("/debug")
def debug():
    files = []
    for root, dirs, fs in os.walk("/app"):
        for f in fs:
            files.append(os.path.join(root, f))
    return jsonify({"files": files, "db_path": DB_PATH})

@app.route("/api/dados")
def api_dados():
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT senioridade, ROUND(AVG(salario_min), 0) FROM vagas GROUP BY senioridade ORDER BY 2")
        rows = cursor.fetchall()
        salario_por_senioridade = {"labels": [r[0] for r in rows], "valores": [r[1] for r in rows]}

        cursor.execute("SELECT vt.tecnologia, COUNT(*) FROM vaga_tecnologia vt GROUP BY vt.tecnologia ORDER BY 2 DESC LIMIT 8")
        rows = cursor.fetchall()
        top_tecnologias = {"labels": [r[0] for r in rows], "valores": [r[1] for r in rows]}

        cursor.execute("SELECT cidade, COUNT(*) FROM vagas GROUP BY cidade ORDER BY 2 DESC")
        rows = cursor.fetchall()
        vagas_por_cidade = {"labels": [r[0] for r in rows], "valores": [r[1] for r in rows]}

        cursor.execute("SELECT modalidade, COUNT(*) FROM vagas GROUP BY modalidade ORDER BY 2 DESC")
        rows = cursor.fetchall()
        modalidade_trabalho = {"labels": [r[0] for r in rows], "valores": [r[1] for r in rows]}

        cursor.execute("SELECT cargo, cidade, senioridade, modalidade, salario_min, salario_max FROM vagas")
        vagas_detalhadas = [{"cargo": r[0], "cidade": r[1], "senioridade": r[2], "modalidade": r[3], "salario_min": r[4], "salario_max": r[5]} for r in cursor.fetchall()]

        conexao.close()
        return jsonify({"salario_por_senioridade": salario_por_senioridade, "top_tecnologias": top_tecnologias, "vagas_por_cidade": vagas_por_cidade, "modalidade_trabalho": modalidade_trabalho, "vagas_detalhadas": vagas_detalhadas})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
