import sqlite3
import json


def conectar():
    return sqlite3.connect("vagas_ti.db")


def salario_por_senioridade(conexao):
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT senioridade, ROUND(AVG(salario_min), 0) AS media
        FROM vagas
        GROUP BY senioridade
        ORDER BY media
    """)
    resultados = cursor.fetchall()
    return {
        "labels": [linha[0] for linha in resultados],
        "valores": [linha[1] for linha in resultados]
    }


def top_tecnologias(conexao, limite=8):
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT vt.tecnologia, COUNT(*) AS qtd
        FROM vaga_tecnologia vt
        GROUP BY vt.tecnologia
        ORDER BY qtd DESC
        LIMIT ?
    """, (limite,))
    resultados = cursor.fetchall()
    return {
        "labels": [linha[0] for linha in resultados],
        "valores": [linha[1] for linha in resultados]
    }


def vagas_por_cidade(conexao):
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT cidade, COUNT(*) AS qtd
        FROM vagas
        GROUP BY cidade
        ORDER BY qtd DESC
    """)
    resultados = cursor.fetchall()
    return {
        "labels": [linha[0] for linha in resultados],
        "valores": [linha[1] for linha in resultados]
    }


def modalidade_trabalho(conexao):
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT modalidade, COUNT(*) AS qtd
        FROM vagas
        GROUP BY modalidade
        ORDER BY qtd DESC
    """)
    resultados = cursor.fetchall()
    return {
        "labels": [linha[0] for linha in resultados],
        "valores": [linha[1] for linha in resultados]
    }


def vagas_detalhadas(conexao):
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT cargo, cidade, senioridade, modalidade, salario_min, salario_max
        FROM vagas
    """)
    resultados = cursor.fetchall()

    return [
        {
            "cargo": linha[0],
            "cidade": linha[1],
            "senioridade": linha[2],
            "modalidade": linha[3],
            "salario_min": linha[4],
            "salario_max": linha[5]
        }
        for linha in resultados
    ]


def main():
    conexao = conectar()

    insights = {
        "salario_por_senioridade": salario_por_senioridade(conexao),
        "top_tecnologias": top_tecnologias(conexao),
        "vagas_por_cidade": vagas_por_cidade(conexao),
        "modalidade_trabalho": modalidade_trabalho(conexao),
        "vagas_detalhadas": vagas_detalhadas(conexao)
    }

    conexao.close()

    with open("../dashboard_web/dados.json", "w", encoding="utf-8") as arquivo:
        json.dump(insights, arquivo, ensure_ascii=False, indent=2)

    print("JSON gerado com sucesso!")
    print("Total de vagas detalhadas:", len(insights["vagas_detalhadas"]))


if __name__ == "__main__":
    main()