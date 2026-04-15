const chatBox = document.querySelector(".chatBox");
const input = document.querySelector(".inputMsg");
const sendBtn = document.querySelector(".sendBtn");
const roomNameDiv = document.querySelector(".roomName");
const onlineDiv = document.querySelector(".onlineMembers");
const typingDiv = document.querySelector(".typingIndicator");

let socket;
let typingTimer;
let typingTimeout;

let username = prompt("Enter username:");
let room = prompt("Enter room name:");

function getTime() {
    return new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit"
    });
}

function addMsg(text, sender, type = "message") {
    const msgDiv = document.createElement("div");

    if (type === "system") {
        msgDiv.classList.add("message", "system");
    } else {
        msgDiv.classList.add(
            "message",
            sender === username ? "user" : "other"
        );
    }

    msgDiv.innerHTML = `${sender}: ${text} 
        <span class="timestamp">${getTime()}</span>`;

    chatBox.insertBefore(msgDiv, typingDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function showTyping(sender) {
    typingDiv.style.display = "flex";
    typingDiv.textContent = `${sender} is typing...`;

    clearTimeout(typingTimeout);

    typingTimeout = setTimeout(() => {
        typingDiv.style.display = "none";
    }, 5000);
}

function connectWebSocket() {
    socket = new WebSocket("ws://127.0.0.1:8765");

    socket.onopen = () => {
        console.log("Connected");

        socket.send(JSON.stringify({
            type: "init",
            username: username
        }));

        socket.send(JSON.stringify({
            type: "join",
            room: room
        }));

        roomNameDiv.textContent = `Room: #${room}`;
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);

        switch (data.type) {
            case "message":
                addMsg(data.text, data.sender);
                break;

            case "room_info":
                onlineDiv.textContent = `Online: ${data.count}`;
                break;

            case "presence":
                console.log("Presence:", data.data);
                break;

            case "typing":
                if (data.sender !== username) {
                    showTyping(data.sender);
                }
                break;

            case "dm":
                addMsg(`[DM] ${data.text}`, data.sender);
                break;
        }
    };

    socket.onclose = () => {
        addMsg("Disconnected from server", "System", "system");
    };

    socket.onerror = () => {
        addMsg("Connection error", "System", "system");
    };
}

function sendMessage() {
    const text = input.value.trim();
    if (!text || socket.readyState !== WebSocket.OPEN) return;

    socket.send(JSON.stringify({
        type: "message",
        text: text
    }));

    input.value = "";

    typingDiv.style.display = "none";
}

input.addEventListener("input", () => {
    clearTimeout(typingTimer);

    typingTimer = setTimeout(() => {
        if (socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({
                type: "typing"
            }));
        }
    }, 300);
});

sendBtn.addEventListener("click", sendMessage);

input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        sendMessage();
    }
});


connectWebSocket();