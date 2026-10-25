/**
 * AI Tutor Chat Client Controller
 * Provides interactive guidance, quick starter prompts, and code-aware tutoring.
 */

document.addEventListener("DOMContentLoaded", () => {
    const chatInput = document.getElementById("chatInputField");
    const sendBtn = document.getElementById("sendChatBtn");

    if (sendBtn) {
        sendBtn.addEventListener("click", sendChatMessage);
    }

    if (chatInput) {
        chatInput.addEventListener("keydown", (e) => {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                sendChatMessage();
            }
        });
    }

    // Quick prompt chips
    const chips = document.querySelectorAll(".prompt-chip");
    chips.forEach(chip => {
        chip.addEventListener("click", () => {
            const promptText = chip.textContent.trim();
            if (chatInput) {
                chatInput.value = promptText;
                sendChatMessage();
            }
        });
    });
});

function sendChatMessage() {
    const chatInput = document.getElementById("chatInputField");
    const message = chatInput ? chatInput.value.trim() : "";
    if (!message) return;

    // Check if code was stored in sessionStorage
    const activeCode = sessionStorage.getItem("c_tutor_active_code") || "";

    // Append user message to UI
    appendMessage(message, "user");
    chatInput.value = "";

    // Show typing indicator
    const typingId = showTypingIndicator();

    fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            message: message,
            code: activeCode
        })
    })
    .then(res => res.json())
    .then(data => {
        removeTypingIndicator(typingId);
        appendMessage(data.reply, "bot");
    })
    .catch(err => {
        removeTypingIndicator(typingId);
        appendMessage("Sorry, I had trouble processing that request. Please try again!", "bot");
    });
}

function appendMessage(text, sender) {
    const messagesContainer = document.getElementById("chatMessages");
    if (!messagesContainer) return;

    const bubble = document.createElement("div");
    bubble.className = `chat-bubble ${sender}`;

    if (sender === "user") {
        bubble.textContent = text;
    } else {
        bubble.innerHTML = renderMarkdown(text);
    }

    messagesContainer.appendChild(bubble);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function showTypingIndicator() {
    const messagesContainer = document.getElementById("chatMessages");
    if (!messagesContainer) return null;

    const id = "typing_" + Date.now();
    const typing = document.createElement("div");
    typing.id = id;
    typing.className = "chat-bubble bot";
    typing.style.opacity = "0.7";
    typing.innerHTML = `<i class="fas fa-robot fa-spin"></i> <em>Tutor is thinking...</em>`;
    messagesContainer.appendChild(typing);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    return id;
}

function removeTypingIndicator(id) {
    if (!id) return;
    const el = document.getElementById(id);
    if (el) el.remove();
}

function renderMarkdown(md) {
    if (!md) return "";
    let html = md;

    // Code blocks ```c ... ```
    html = html.replace(/```(?:c|C)?\n([\s\S]*?)```/g, (match, p1) => {
        return `<pre style="background: #080d1a; padding: 12px; border-radius: 6px; font-family: var(--font-mono); font-size: 13px; color: #38bdf8; overflow-x: auto; margin: 10px 0; border: 1px solid rgba(56,189,248,0.2);"><code>${escapeHtml(p1.trim())}</code></pre>`;
    });

    // Inline code `...`
    html = html.replace(/`([^`]+)`/g, '<code style="background: rgba(56,189,248,0.15); color: #38bdf8; padding: 2px 6px; border-radius: 4px; font-family: var(--font-mono); font-size: 12.5px;">$1</code>');

    // Headers
    html = html.replace(/^### (.*$)/gim, '<h4 style="color:#fff; margin: 12px 0 6px; font-size: 15px;">$1</h4>');
    html = html.replace(/^## (.*$)/gim, '<h3 style="color:#38bdf8; margin: 14px 0 8px; font-size: 16px;">$1</h3>');

    // Bold
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Italics
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');

    // Line breaks
    html = html.replace(/\n\n/g, '<p style="margin-bottom: 8px;"></p>');
    html = html.replace(/\n/g, '<br/>');

    return html;
}

function escapeHtml(text) {
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
}
