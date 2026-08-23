import sqlite3
import csv

conexao = sqlite3.connect("vagas_ti.db")
cursor = conexao.cursor()

with open("../data/vagas_ti.csv", encoding="utf-8") as arquivo:
    leitor = csv.DictReader(arquivo)

    for linha in leitor:
        cursor.execute(
    "INSERT INTO vagas (id, cargo, cidade, senioridade, salario_min, salario_max, modalidade) VALUES (?, ?, ?, ?, ?, ?, ?)",
    (linha["id"], linha["cargo"], linha["cidade"], linha["senioridade"], linha["salario_min"], linha["salario_max"], linha["modalidade"])
)

with open("../data/vaga_tecnologias.csv", encoding="utf-8") as arquivo:
    leitor = csv.DictReader(arquivo)

    for linha in leitor:
        cursor.execute(
            "INSERT INTO vaga_tecnologia (vaga_id, tecnologia) VALUES (?, ?)",
            (linha["vaga_id"], linha["tecnologia"])
        )

conexao.commit()
conexao.close()

print("Dados carregados no banco com sucesso!")