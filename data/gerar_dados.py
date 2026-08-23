import random
import csv

random.seed(42)

AREAS = [
    ("Desenvolvimento Backend", 22),
    ("Desenvolvimento Frontend", 14),
    ("Dados / BI", 16),
    ("Suporte / Infraestrutura", 18),
]

CIDADES = [
    ("São Paulo - SP", 30),
    ("Rio de Janeiro - RJ", 11),
    ("Remoto (Brasil)", 13),
]

SENIORIDADES = [
    ("Júnior", 30),
    ("Pleno", 32),
    ("Sênior", 19),
]

FAIXA_SALARIAL = {
    "Júnior": (2500, 4800),
    "Pleno": (5000, 9500),
    "Sênior": (9500, 17000),
}

TECNOLOGIAS_POR_AREA = {
    "Desenvolvimento Backend": ["Python", "Java", "Node.js", "PostgreSQL", "Docker", "AWS"],
    "Desenvolvimento Frontend": ["JavaScript", "React", "TypeScript", "CSS"],
    "Dados / BI": ["SQL", "Python", "Power BI", "Excel Avançado"],
    "Suporte / Infraestrutura": ["Active Directory", "Windows Server", "ITIL", "Redes"],
}

MODALIDADES = [
    ("Remoto", 46),
    ("Híbrido", 36),
    ("Presencial", 18),
]


def sorteio_ponderado(tabela):
    valores = [item[0] for item in tabela]
    pesos = [item[1] for item in tabela]
    resultado = random.choices(valores, weights=pesos, k=1)
    return resultado[0]


def gerar_vaga():
    senioridade = sorteio_ponderado(SENIORIDADES)
    faixa_min, faixa_max = FAIXA_SALARIAL[senioridade]

    salario_min = random.randint(faixa_min, int(faixa_min * 1.1))
    salario_max = random.randint(int(faixa_max * 0.9), faixa_max)

    cargo = sorteio_ponderado(AREAS)
    tecnologias_da_area = TECNOLOGIAS_POR_AREA[cargo]
    qtd_tecnologias = random.randint(2, 4)
    tecnologias_sorteadas = random.sample(tecnologias_da_area, k=qtd_tecnologias)

    modalidade = sorteio_ponderado(MODALIDADES)

    vaga = {
        "cargo": cargo,
        "cidade": sorteio_ponderado(CIDADES),
        "senioridade": senioridade,
        "salario_min": salario_min,
        "salario_max": salario_max,
        "modalidade": modalidade,
        "tecnologias": tecnologias_sorteadas,
    }
    return vaga


lista_de_vagas = []
for i in range(3000):
    nova_vaga = gerar_vaga()
    lista_de_vagas.append(nova_vaga)

print("Total de vagas geradas:", len(lista_de_vagas))
print("Exemplo da primeira vaga:", lista_de_vagas[0])
print("Exemplo da última vaga:", lista_de_vagas[-1])

for i, vaga in enumerate(lista_de_vagas, start=1):
    vaga["id"] = i

campos_vagas = ["id", "cargo", "cidade", "senioridade", "salario_min", "salario_max", "modalidade"]

with open("vagas_ti.csv", "w", newline="", encoding="utf-8") as arquivo:
    escritor = csv.DictWriter(arquivo, fieldnames=campos_vagas, extrasaction="ignore")
    escritor.writeheader()
    escritor.writerows(lista_de_vagas)


with open("vaga_tecnologias.csv", "w", newline="", encoding="utf-8") as arquivo:
    escritor = csv.writer(arquivo)
    escritor.writerow(["vaga_id", "tecnologia"])

    for vaga in lista_de_vagas:
        for tecnologia in vaga["tecnologias"]:
            escritor.writerow([vaga["id"], tecnologia])

print("Arquivos CSV salvos com sucesso!")