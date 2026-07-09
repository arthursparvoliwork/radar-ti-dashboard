import sqlite3
import csv

conexao = sqlite3.connect("vagas_ti.db")
cursor = conexao.cursor()

with open("../data/vagas_ti.csv", encoding="utf-8") as arquivo:
    leitor = csv.DictReader(arquivo)

    for linha in leitor:
        cursor.execute(
            "INSERT INTO vagas (cargo, cidade, senioridade, salario_min, salario_max) VALUES (?, ?, ?, ?, ?)",
            (linha["cargo"], linha["cidade"], linha["senioridade"], linha["salario_min"], linha["salario_max"])
        )

conexao.commit()
conexao.close()

print("Dados carregados no banco com sucesso!")