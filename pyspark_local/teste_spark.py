from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("JoinTecnologias").getOrCreate()

vagas = spark.read.csv("../data/vagas_ti.csv", header=True, inferSchema=True)
tecnologias = spark.read.csv("../data/vaga_tecnologias.csv", header=True, inferSchema=True)

vagas.createOrReplaceTempView("vagas")
tecnologias.createOrReplaceTempView("vaga_tecnologia")

resultado = spark.sql("""
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

resultado.show()

spark.stop()