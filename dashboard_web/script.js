

const canvasParticulas = document.getElementById("fundoParticulas");
const ctxParticulas = canvasParticulas.getContext("2d");
let dadosGlobais = null;

canvasParticulas.width = window.innerWidth;
canvasParticulas.height = window.innerHeight;

const particulas = [];
const quantidadeParticulas = 60;

for (let i = 0; i < quantidadeParticulas; i++) {
    particulas.push({
        x: Math.random() * canvasParticulas.width,
        y: Math.random() * canvasParticulas.height,
        raio: Math.random() * 2 + 1,
        velocidadeX: (Math.random() - 0.5) * 0.5,
        velocidadeY: (Math.random() - 0.5) * 0.5
    });
}

const mouse = { x: null, y: null, raioAtivo: 150 };

window.addEventListener("mousemove", (evento) => {
    mouse.x = evento.clientX;
    mouse.y = evento.clientY;
});

function desenharParticulas() {
    ctxParticulas.clearRect(0, 0, canvasParticulas.width, canvasParticulas.height);

    for (const particula of particulas) {
        particula.x += particula.velocidadeX;
        particula.y += particula.velocidadeY;

        if (particula.x < 0 || particula.x > canvasParticulas.width) {
            particula.velocidadeX *= -1;
        }
        if (particula.y < 0 || particula.y > canvasParticulas.height) {
            particula.velocidadeY *= -1;
        }

        if (mouse.x !== null) {
            const dx = particula.x - mouse.x;
            const dy = particula.y - mouse.y;
            const distancia = Math.sqrt(dx * dx + dy * dy);

            if (distancia < mouse.raioAtivo) {
                const forca = (mouse.raioAtivo - distancia) / mouse.raioAtivo;
                particula.x += (dx / distancia) * forca * 3;
                particula.y += (dy / distancia) * forca * 3;
            }
        }

        ctxParticulas.beginPath();
        ctxParticulas.arc(particula.x, particula.y, particula.raio, 0, Math.PI * 2);
        ctxParticulas.fillStyle = "rgba(69, 194, 181, 0.6)";
        ctxParticulas.fill();
    }

    const distanciaMaxima = 130;

    for (let i = 0; i < particulas.length; i++) {
        for (let j = i + 1; j < particulas.length; j++) {
            const dx = particulas[i].x - particulas[j].x;
            const dy = particulas[i].y - particulas[j].y;
            const distancia = Math.sqrt(dx * dx + dy * dy);

            if (distancia < distanciaMaxima) {
                const opacidade = 1 - (distancia / distanciaMaxima);

                ctxParticulas.beginPath();
                ctxParticulas.moveTo(particulas[i].x, particulas[i].y);
                ctxParticulas.lineTo(particulas[j].x, particulas[j].y);
                ctxParticulas.strokeStyle = `rgba(69, 194, 181, ${opacidade * 0.3})`;
                ctxParticulas.lineWidth = 1;
                ctxParticulas.stroke();
            }
        }
    }

    requestAnimationFrame(desenharParticulas);
}

desenharParticulas();


const iconesTech = [
    "fa-brands fa-python", "fa-brands fa-js", "fa-brands fa-java",
    "fa-brands fa-html5", "fa-brands fa-css3-alt", "fa-brands fa-react",
    "fa-brands fa-node-js", "fa-brands fa-docker", "fa-brands fa-git-alt",
    "fa-brands fa-github", "fa-brands fa-vuejs", "fa-brands fa-angular",
    "fa-brands fa-php", "fa-brands fa-aws", "fa-brands fa-linux",
    "fa-brands fa-windows", "fa-brands fa-apple", "fa-brands fa-android",
    "fa-solid fa-database", "fa-solid fa-server", "fa-solid fa-cloud",
    "fa-solid fa-terminal", "fa-solid fa-microchip", "fa-solid fa-code",
    "fa-solid fa-network-wired", "fa-solid fa-robot"
];

const containerIcones = document.getElementById("icconesFundo");
const quantidadeIcones = 22;

for (let i = 0; i < quantidadeIcones; i++) {
    const icone = document.createElement("i");
    const classeEscolhida = iconesTech[Math.floor(Math.random() * iconesTech.length)];

    icone.className = `${classeEscolhida} icone-flutuante`;
    icone.style.top = `${Math.random() * 95}%`;
    icone.style.left = `${Math.random() * 95}%`;
    icone.style.fontSize = `${Math.random() * 24 + 20}px`;
    icone.style.animationDelay = `${Math.random() * 5}s`;
    icone.style.animationDuration = `${Math.random() * 4 + 6}s`;

    containerIcones.appendChild(icone);
}

const elementosReveal = document.querySelectorAll(".reveal");

const observador = new IntersectionObserver((entradas) => {
    entradas.forEach((entrada) => {
        if (entrada.isIntersecting) {
            anime.animate(entrada.target, {
                opacity: [0, 1],
                translateY: [40, 0],
                scale: [0.96, 1],
                duration: 900,
                ease: "outExpo"
            });
            observador.unobserve(entrada.target);
        }
    });
});

elementosReveal.forEach((elemento) => {
    observador.observe(elemento);
});


async function carregarDashboard() {
   const resposta = await fetch("https://radar-ti-dashboard-production.up.railway.app/api/dados");
    dadosGlobais = await resposta.json();

    refGraficoSalarios = criarGraficoBarras("graficoSalarios", dadosGlobais.salario_por_senioridade, "Salário médio mínimo (R$)", "#45C2B5");
    criarListaRanking("listaTecnologias", dadosGlobais.top_tecnologias);
    refGraficoCidades = criarGraficoBarras("graficoCidades", dadosGlobais.vagas_por_cidade, "Vagas", "#E0664F");
    refGraficoModalidade = criarGraficoRosca("graficoModalidade", dadosGlobais.modalidade_trabalho);

    aplicarFiltros();
}

function aplicarFiltros() {
    const senioridadeEscolhida = document.getElementById("filtroSenioridade").value;
    const modalidadeEscolhida = document.getElementById("filtroModalidade").value;

    const vagasFiltradas = dadosGlobais.vagas_detalhadas.filter((vaga) => {
        const passaSenioridade = senioridadeEscolhida === "todos" || vaga.senioridade === senioridadeEscolhida;
        const passaModalidade = modalidadeEscolhida === "todos" || vaga.modalidade === modalidadeEscolhida;
        return passaSenioridade && passaModalidade;
    });

    atualizarCards(vagasFiltradas);
    recalcularGraficoSalarios(vagasFiltradas);
    recalcularGraficoCidades(vagasFiltradas);
    recalcularGraficoModalidade(vagasFiltradas);
}

function atualizarCards(vagas) {
    const totalVagas = vagas.length;

    const somaMedias = vagas.reduce((acumulado, vaga) => {
        return acumulado + (vaga.salario_min + vaga.salario_max) / 2;
    }, 0);
    const salarioMedio = totalVagas > 0 ? Math.round(somaMedias / totalVagas) : 0;

    const vagasRemotas = vagas.filter((vaga) => vaga.modalidade === "Remoto").length;
    const percentualRemoto = totalVagas > 0 ? (vagasRemotas / totalVagas) * 100 : 0;

    document.getElementById("contadorTotalVagas").textContent = totalVagas.toLocaleString("pt-BR");
    document.getElementById("contadorSalarioMedio").textContent = salarioMedio.toLocaleString("pt-BR");
    document.getElementById("contadorPercentualRemoto").textContent = percentualRemoto.toLocaleString("pt-BR", { minimumFractionDigits: 1, maximumFractionDigits: 1 });

    anime.animate(".contador", {
        scale: [1.3, 1],
        duration: 400,
        ease: "outElastic(1, .6)"
    });
}
function criarGraficoBarras(idCanvas, dados, rotulo, cor) {
    const ctx = document.getElementById(idCanvas);

    return new Chart(ctx, {
        type: "bar",
        data: {
            labels: dados.labels,
            datasets: [{
                label: rotulo,
                data: dados.valores,
                backgroundColor: cor
            }]
        },
        options: {
            maintainAspectRatio: false
        }
    });
}
function criarListaRanking(idContainer, dados) {
    const container = document.getElementById(idContainer);
    const valorMaximo = Math.max(...dados.valores);

    dados.labels.forEach((nome, indice) => {
        const valor = dados.valores[indice];
        const porcentagem = (valor / valorMaximo) * 100;

        const item = document.createElement("div");
        item.className = "item-ranking";

        item.innerHTML = `
            <div class="item-ranking-topo">
                <span>${nome}</span>
                <span>${valor}</span>
            </div>
            <div class="barra-fundo">
                <div class="barra-preenchida" style="width: 0%"></div>
            </div>
        `;

        container.appendChild(item);

        setTimeout(() => {
            item.querySelector(".barra-preenchida").style.width = porcentagem + "%";
        }, 100);
    });

    anime.animate(".item-ranking", {
        opacity: [0, 1],
        translateX: [-20, 0],
        delay: anime.stagger(80),
        duration: 500,
        ease: "outQuad"
    });
}

function criarGraficoRosca(idCanvas, dados) {
    const ctx = document.getElementById(idCanvas);

    return new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: dados.labels,
            datasets: [{
                data: dados.valores,
                backgroundColor: ["#45C2B5", "#F2A93B", "#E0664F"],
                borderColor: "#0D1117",
                borderWidth: 3
            }]
        },
        options: {
            maintainAspectRatio: false
        }
    });
}

function animarContadores() {
    document.querySelectorAll(".contador").forEach((elemento) => {
        const valorFinal = parseFloat(elemento.getAttribute("data-valor-final"));
        const casasDecimais = parseInt(elemento.getAttribute("data-decimal")) || 0;
        const duracao = 1500;
        const inicio = performance.now();

        function atualizar(agora) {
            const progresso = Math.min((agora - inicio) / duracao, 1);
            const valorAtual = valorFinal * progresso;

            elemento.textContent = valorAtual.toLocaleString("pt-BR", {
                minimumFractionDigits: casasDecimais,
                maximumFractionDigits: casasDecimais
            });

            if (progresso < 1) {
                requestAnimationFrame(atualizar);
            }
        }

        requestAnimationFrame(atualizar);
    });
}

carregarDashboard();
animarContadores();

document.getElementById("filtroSenioridade").addEventListener("change", aplicarFiltros);
document.getElementById("filtroModalidade").addEventListener("change", aplicarFiltros);

function recalcularGraficoSalarios(vagas) {
    const senioridades = ["Júnior", "Pleno", "Sênior"];

    const medias = senioridades.map((nivel) => {
        const vagasDoNivel = vagas.filter((vaga) => vaga.senioridade === nivel);

        if (vagasDoNivel.length === 0) {
            return 0;
        }

        const soma = vagasDoNivel.reduce((acumulado, vaga) => acumulado + vaga.salario_min, 0);
        return Math.round(soma / vagasDoNivel.length);
    });

    refGraficoSalarios.data.labels = senioridades;
    refGraficoSalarios.data.datasets[0].data = medias;
    refGraficoSalarios.update();
}
function recalcularGraficoCidades(vagas) {
    const cidades = ["São Paulo - SP", "Remoto (Brasil)", "Rio de Janeiro - RJ"];

    const contagens = cidades.map((cidade) => {
        return vagas.filter((vaga) => vaga.cidade === cidade).length;
    });

    refGraficoCidades.data.labels = cidades;
    refGraficoCidades.data.datasets[0].data = contagens;
    refGraficoCidades.update();
}

function recalcularGraficoModalidade(vagas) {
    const modalidades = ["Remoto", "Híbrido", "Presencial"];

    const contagens = modalidades.map((modalidade) => {
        return vagas.filter((vaga) => vaga.modalidade === modalidade).length;
    });

    refGraficoModalidade.data.labels = modalidades;
    refGraficoModalidade.data.datasets[0].data = contagens;
    refGraficoModalidade.update();
}

anime.animate(".card", {
    opacity: [0, 1],
    translateY: [30, 0],
    delay: anime.stagger(120),
    duration: 700,
    ease: "outExpo"
});

anime.animate(".decoracao-codigo", {
    rotate: 360,
    duration: 20000,
    loop: true,
    ease: "linear"
}); 

document.querySelectorAll(".botao-social").forEach((botao) => {
    botao.addEventListener("mouseenter", () => {
        anime.animate(botao, {
            scale: [1, 1.15, 1],
            duration: 600,
            ease: "outElastic(1, .5)"
        });
    });
});
