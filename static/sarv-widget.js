(function () {
  // Prevent duplicate initialization
  if (window.SarvWidgetLoaded) return;
  window.SarvWidgetLoaded = true;

  // Retrieve API Key and Gateway URL from the script tag attributes
  const currentScript = document.currentScript;
  const SARV_KEY = currentScript ? currentScript.getAttribute("data-key") || "" : "";
  const SARV_HOST = currentScript ? currentScript.getAttribute("data-host") || "https://sarv-ai-os.onrender.com" : "https://sarv-ai-os.onrender.com";

  // Create Widget Elements
  const container = document.createElement("div");
  container.id = "sarv-widget-container";
  container.innerHTML = `
    <style>
      #sarv-bubble {
        position: fixed;
        bottom: 24px;
        right: 24px;
        width: 56px;
        height: 56px;
        border-radius: 50%;
        background: linear-gradient(135deg, #00f0ff, #7000ff);
        box-shadow: 0 4px 16px rgba(0, 240, 255, 0.4);
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 999999;
        transition: transform 0.2s ease;
      }
      #sarv-bubble:hover { transform: scale(1.08); }
      #sarv-bubble svg { width: 28px; height: 28px; fill: #ffffff; }

      #sarv-chat-box {
        position: fixed;
        bottom: 90px;
        right: 24px;
        width: 360px;
        height: 480px;
        background: #0b0f19;
        border: 1px solid #1f2937;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.6);
        display: none;
        flex-direction: column;
        overflow: hidden;
        z-index: 999999;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      }

      .sarv-header {
        background: #111827;
        border-bottom: 1px solid #1f2937;
        padding: 14px 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
      .sarv-header h3 { margin: 0; font-size: 14px; color: #00f0ff; letter-spacing: 1px; }
      .sarv-close { cursor: pointer; color: #9ca3af; font-size: 18px; font-weight: bold; }

      .sarv-messages {
        flex: 1;
        padding: 14px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 10px;
      }

      .sarv-msg {
        max-width: 80%;
        padding: 10px 14px;
        border-radius: 12px;
        font-size: 13px;
        line-height: 1.4;
        word-wrap: break-word;
      }
      .sarv-msg.bot {
        align-self: flex-start;
        background: #1f2937;
        color: #f3f4f6;
        border: 1px solid #374151;
      }
      .sarv-msg.user {
        align-self: flex-end;
        background: linear-gradient(135deg, #00f0ff, #7000ff);
        color: #ffffff;
      }

      .sarv-input-area {
        display: flex;
        padding: 10px;
        background: #111827;
        border-top: 1px solid #1f2937;
        gap: 8px;
      }
      .sarv-input-area input {
        flex: 1;
        background: #070a11;
        border: 1px solid #374151;
        color: #f3f4f6;
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 13px;
        outline: none;
      }
      .sarv-input-area input:focus { border-color: #00f0ff; }
      .sarv-input-area button {
        background: #00f0ff;
        border: none;
        color: #0b0f19;
        font-weight: bold;
        padding: 8px 14px;
        border-radius: 8px;
        cursor: pointer;
      }
    </style>

    <div id="sarv-bubble">
      <svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/></svg>
    </div>

    <div id="sarv-chat-box">
      <div class="sarv-header">
        <h3>SARV AI OS</h3>
        <span class="sarv-close">&times;</span>
      </div>
      <div class="sarv-messages" id="sarv-msg-list">
        <div class="sarv-msg bot">Hello! I am SARV AI OS. How can I assist you today?</div>
      </div>
      <div class="sarv-input-area">
        <input type="text" id="sarv-chat-input" placeholder="Type a message..." />
        <button id="sarv-send-btn">Send</button>
      </div>
    </div>
  `;
  document.body.appendChild(container);

  // Widget Event Handlers
  const bubble = document.getElementById("sarv-bubble");
  const chatBox = document.getElementById("sarv-chat-box");
  const closeBtn = chatBox.querySelector(".sarv-close");
  const sendBtn = document.getElementById("sarv-send-btn");
  const chatInput = document.getElementById("sarv-chat-input");
  const msgList = document.getElementById("sarv-msg-list");

  bubble.onclick = () => {
    chatBox.style.display = chatBox.style.display === "flex" ? "none" : "flex";
  };
  closeBtn.onclick = () => { chatBox.style.display = "none"; };

  async function sendMessage() {
    const text = chatInput.value.trim();
    if (!text) return;

    appendMsg(text, "user");
    chatInput.value = "";

    try {
      const res = await fetch(`${SARV_HOST}/v1/execute`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${SARV_KEY}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ command: text })
      });
      const data = await res.json();
      appendMsg(res.ok ? data.result : `Error: ${data.detail || "Authentication Failed"}`, "bot");
    } catch (err) {
      appendMsg(`Network error connecting to SARV: ${err.message}`, "bot");
    }
  }

  function appendMsg(content, sender) {
    const msg = document.createElement("div");
    msg.className = `sarv-msg ${sender}`;
    msg.innerText = content;
    msgList.appendChild(msg);
    msgList.scrollTop = msgList.scrollHeight;
  }

  sendBtn.onclick = sendMessage;
  chatInput.onkeydown = (e) => { if (e.key === "Enter") sendMessage(); };
})();