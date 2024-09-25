// Itens fixos com nomes fixos (aparecem de maneira fixa na tela)
const itensFixos = [
    { nome: "Óculos de proteção", quantidade: 30 },
    { nome: "Led", quantidade: 30 },
    { nome: "Registros", quantidade: 30 },
    { nome: "TAG", quantidade: 30 },
    { nome: "Protoboard", quantidade: 30 },
    { nome: "Leitor RFID", quantidade: 30 },
    { nome: "Fonte de alimentação USB tipo C", quantidade: 30 },
    { nome: "Speaker", quantidade: 30 },
    { nome: "Sensor de luminosidade", quantidade: 30 },
    { nome: "Arduino", quantidade: 30 },
    { nome: "Raspberry", quantidade: 30 },
    { nome: "Kit Discovery", quantidade: 30 },
    { nome: "Multímetro", quantidade: 30 },
    { nome: "Cabo colorido macho/macho", quantidade: 30 },
    { nome: "Cabo colorido macho/fêmea", quantidade: 30 },
    { nome: "Pulseira antiestática", quantidade: 30 },
    { nome: "Kit solda", quantidade: 30 },
    { nome: "Sensor de umidade do solo", quantidade: 30 },
    { nome: "Lupa", quantidade: 30 },
    { nome: "Módulo Wi-Fi para Arduino", quantidade: 30 },
    { nome: "Protoboard", quantidade: 30 },
    { nome: "Cabo conversor HD", quantidade: 30 },
    { nome: "Buzzer", quantidade: 30 },
    { nome: "Sensor ultra sônico", quantidade: 30 },
    { nome: "Kit sensores para Arduino", quantidade: 30 }
];

// Função de login
document.getElementById("login-form")?.addEventListener("submit", function(event) {
    event.preventDefault();
    
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    if (username === "Aluno" && password === "Senha") {
        window.location.href = "main.html";
    } else {
        document.getElementById("error-message").innerText = "Usuário ou senha incorretos.";
    }
});

// Função para carregar os itens fixos na tela principal
function carregarItens() {
    const itemList = document.getElementById('item-list');

    if (itemList) {
        itensFixos.forEach(item => {
            const itemBox = document.createElement('div');
            itemBox.classList.add('item-box');

            itemBox.innerHTML = `
                <h3>${item.nome}</h3>
                <p>Quantidade disponível: ${item.quantidade}</p>
                <button onclick="mostrarRetiradas('${item.nome}')">Ver retiradas</button>
            `;

            itemList.appendChild(itemBox);
        });
    }
}

// Função para exibir os alunos que retiraram o item (API fictícia)
function mostrarRetiradas(item) {
    // Simulação de uma chamada de API para buscar alunos
    const alunos = ["João", "Maria", "Pedro"];
    alert(`Alunos que retiraram ${item}: ${alunos.join(', ')}`);
}

// Função de logoff
document.getElementById('logoff-btn')?.addEventListener('click', function() {
    window.location.href = 'index.html';
});

// Carregar itens ao carregar a página principal
window.onload = carregarItens;


