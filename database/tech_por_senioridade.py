import sqlite3

conexao = sqlite3.connect("vagas_ti.db")
cursor = conexao.cursor()

cursor.execute("""
    SELECT
        vt.tecnologia,
        COUNT(*) AS qtd_vagas
    FROM vaga_tecnologia vt
    JOIN vagas v ON vt.vaga_id = v.id
    WHERE v.senioridade = 'Sênior'
    GROUP BY vt.tecnologia
    ORDER BY qtd_vagas DESC
    LIMIT 5
""")

resultados = cursor.fetchall()
for linha in resultados:
    print(linha)

conexao.close()