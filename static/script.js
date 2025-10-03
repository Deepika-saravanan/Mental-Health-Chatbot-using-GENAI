async function sendMessage() {
    const inputBox = document.getElementById("user-input");
    const message = inputBox.value.trim();
    if (!message) return;

    const chatLog = document.getElementById("chat-log");

    const userBubble = document.createElement("div");
    userBubble.className = "user-message";
    userBubble.textContent = message;
    chatLog.appendChild(userBubble);

    inputBox.value = "";

    chatLog.scrollTop = chatLog.scrollHeight;

    const response = await fetch("/ask", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message})
    });

    const data = await response.json();

    const botBubble = document.createElement("div");
    botBubble.className = "bot-message";
    botBubble.textContent = data.answer;
    chatLog.appendChild(botBubble);

    chatLog.scrollTop = chatLog.scrollHeight;
}