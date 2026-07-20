document.addEventListener("DOMContentLoaded", () => {
    const sendBtn = document.getElementById("sendBtn");
    const userInput = document.getElementById("userInput");
    const chatBox = document.getElementById("chatBox");

    // Maintain conversation history in memory
    let conversationHistory = [];

    async function sendMessage() {
        const text = userInput.value.trim();
        if (!text) return;

        // 1. Render user message in UI
        appendMessage(text, "user-message");
        userInput.value = "";

        // 2. Add temporary loading message
        const loadingDiv = appendMessage("Thinking...", "bot-message");

        try {
            const res = await fetch("http://127.0.0.1:8000/chat", {
                method: "POST",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    question: text,
                    history: conversationHistory
                })
            });

            if (!res.ok) {
                const errText = await res.text();
                throw new Error(`HTTP ${res.status}: ${errText}`);
            }

            const data = await res.json();

            // 3. Update loading text with actual reply
            loadingDiv.innerText = data.answer;

            // 4. Update memory history
            conversationHistory.push({ role: "user", parts: [text] });
            conversationHistory.push({ role: "model", parts: [data.answer] });

        } catch (err) {
            console.error("Error:", err);
            loadingDiv.innerText = `Error: Couldn't connect to backend server.`;
        }
    }

    function appendMessage(text, className) {
        const msgDiv = document.createElement("div");
        msgDiv.className = `message ${className}`;
        msgDiv.innerText = text;
        chatBox.appendChild(msgDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
        return msgDiv;
    }

    sendBtn.addEventListener("click", sendMessage);

    // Allow pressing Enter key to send
    userInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") sendMessage();
    });
});