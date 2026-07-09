import sqlite3

conexao = sqlite3.connect("vagas_ti.db")
cursor = conexao.cursor()

cursor.execute("""
    SELECT cidade, COUNT(*)
    FROM vagas
    GROUP BY cidade
    ORDER BY COUNT(*) DESC
""")

resultados = cursor.fetchall()
for linha in resultados:
    print(linha)

conexao.close()