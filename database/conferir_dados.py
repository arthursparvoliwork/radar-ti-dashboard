import sqlite3

conexao = sqlite3.connect("vagas_ti.db")
cursor = conexao.cursor()

cursor.execute("SELECT COUNT(*) FROM vagas")
total = cursor.fetchone()
print("Total de linhas na tabela:", total[0])

cursor.execute("SELECT * FROM vagas LIMIT 3")
primeiras_linhas = cursor.fetchall()
for linha in primeiras_linhas:
    print(linha)

conexao.close()