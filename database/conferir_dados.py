import sqlite3

conexao = sqlite3.connect("vagas_ti.db")
cursor = conexao.cursor()

cursor.execute("SELECT COUNT(*) FROM vagas")
total_vagas = cursor.fetchone()
print("Total de linhas em 'vagas':", total_vagas[0])

cursor.execute("SELECT COUNT(*) FROM vaga_tecnologia")
total_tecnologias = cursor.fetchone()
print("Total de linhas em 'vaga_tecnologia':", total_tecnologias[0])

cursor.execute("SELECT * FROM vagas LIMIT 2")
print("\nExemplo de vagas:")
for linha in cursor.fetchall():
    print(linha)

cursor.execute("SELECT * FROM vaga_tecnologia WHERE vaga_id = 1")
print("\nTecnologias da vaga 1:")
for linha in cursor.fetchall():
    print(linha)

conexao.close()