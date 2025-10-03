async function sendMessage() {
    const inputBox = document.getElementById("user-input");
    const message = inputBox.value.trim();
    if (!message) return;

    const chatLog = document.getElementById("chat-log");

    // Add user message
    const userBubble = document.createElement("div");
    userBubble.className = "user-message";
    userBubble.textContent = message;
    chatLog.appendChild(userBubble);

    inputBox.value = "";

    // Scroll to bottom
    chatLog.scrollTop = chatLog.scrollHeight;

    // Send to backend
    const response = await fetch("/ask", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message})
    });

    const data = await response.json();

    // Add bot message
    const botBubble = document.createElement("div");
    botBubble.className = "bot-message";
    botBubble.textContent = data.answer;
    chatLog.appendChild(botBubble);

    // Scroll to bottom
    chatLog.scrollTop = chatLog.scrollHeight;
}