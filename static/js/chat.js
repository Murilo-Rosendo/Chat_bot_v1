const chatForm = document.getElementById("chat-form");
const chatBox = document.getElementById("chat-box");
const input = document.getElementById("pergunta");

function scrollToBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
}

function addMessage(text, type) {
    const message = document.createElement("div");
    message.className = `msg ${type}-msg`;
    message.textContent = text;
    chatBox.appendChild(message);
    scrollToBottom();
    return message;
}

function addQuickActions() {
    const actions = document.createElement("div");
    actions.className = "quick-actions";

    ["Ver saldo", "Fazer Pix", "Bloquear cartão"].forEach((label) => {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "quick-action";
        button.textContent = label;
        button.addEventListener("click", () => sendMessage(label));
        actions.appendChild(button);
    });

    chatBox.appendChild(actions);
    scrollToBottom();
}

function showTyping() {
    const typing = document.createElement("div");
    typing.className = "msg bot-msg typing";
    typing.setAttribute("aria-label", "Murilo Bot está digitando");
    typing.innerHTML = "<span></span><span></span><span></span>";
    chatBox.appendChild(typing);
    scrollToBottom();
    return typing;
}

async function sendMessage(text) {
    const texto = text.trim();
    if (!texto) return;

    addMessage(texto, "user");
    input.value = "";
    input.focus();

    const typing = showTyping();
    const formData = new FormData();
    formData.append("texto", texto);

    try {
        const response = await fetch("/perguntar", {
            method: "POST",
            body: formData
        });
        const data = await response.json();
        typing.remove();
        addMessage(data.resposta, "bot");
    } catch (error) {
        typing.remove();
        addMessage("Não consegui responder agora. Verifique se o servidor está rodando.", "bot");
    }
}

addMessage("Olá! Eu sou o Murilo Bot. Posso ajudar com saldo, Pix, cartão, extrato, pagamentos e segurança.", "bot");
addQuickActions();

chatForm.addEventListener("submit", (event) => {
    event.preventDefault();
    sendMessage(input.value);
});
