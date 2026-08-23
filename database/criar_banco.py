import sqlite3

conexao = sqlite3.connect("vagas_ti.db")
cursor = conexao.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS vagas (
        id INTEGER PRIMARY KEY,
        cargo TEXT,
        cidade TEXT,
        senioridade TEXT,
        salario_min INTEGER,
        salario_max INTEGER,
        modalidade TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS vaga_tecnologia (
        vaga_id INTEGER,
        tecnologia TEXT,
        FOREIGN KEY (vaga_id) REFERENCES vagas(id)
    )
""")

conexao.commit()
conexao.close()

print("Banco de dados e tabelas criados com sucesso!")