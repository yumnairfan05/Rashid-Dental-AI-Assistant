document.addEventListener("DOMContentLoaded", () => {
    const askBtn = document.getElementById("askBtn");
    const userInput = document.getElementById("userInput");
    const responseDiv = document.getElementById("response");

    if (!askBtn) {
        console.error("Button element #askBtn missing from HTML");
        return;
    }

    askBtn.addEventListener("click", async () => {
        const question = userInput.value.trim();

        if (!question) {
            alert("Please type a question first.");
            return;
        }

        responseDiv.innerText = "Thinking... Please wait.";

        try {
            const res = await fetch("http://127.0.0.1:8000/chat", {
                method: "POST",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    question: question,
                    context: ""
                })
            });

            if (!res.ok) {
                const errText = await res.text();
                throw new Error(`Server returned HTTP ${res.status}: ${errText}`);
            }

            const data = await res.json();
            responseDiv.innerText = data.answer || "No response received.";

        } catch (error) {
            console.error("Fetch failure:", error);
            responseDiv.innerText = `Error connecting to backend:\n${error.message}\n\nMake sure Uvicorn is running on http://127.0.0.1:8000`;
        }
    });
});