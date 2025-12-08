document.addEventListener('DOMContentLoaded', () => {
    // Initialize Particles.js
    particlesJS('particles-js', {
        "particles": {
            "number": { "value": 80, "density": { "enable": true, "value_area": 800 } },
            "color": { "value": "#ffffff" },
            "shape": { "type": "circle" },
            "opacity": { "value": 0.5, "random": false },
            "size": { "value": 3, "random": true },
            "line_linked": { "enable": true, "distance": 150, "color": "#ffffff", "opacity": 0.4, "width": 1 },
            "move": { "enable": true, "speed": 6, "direction": "none", "random": false, "straight": false, "out_mode": "out", "bounce": false }
        },
        "interactivity": {
            "detect_on": "canvas",
            "events": {
                "onhover": { "enable": true, "mode": "repulse" },
                "onclick": { "enable": true, "mode": "push" },
                "resize": true
            }
        },
        "retina_detect": true
    });

    // SocketIO Connection
    const socket = io();
    const statusText = document.getElementById('status-text');
    const statusCircle = document.querySelector('.circle');
    const chatBox = document.getElementById('chat-box');
    const micBtn = document.getElementById('mic-btn');
    const textInput = document.getElementById('text-input');
    const sendBtn = document.getElementById('send-btn');

    micBtn.addEventListener('click', () => {
        socket.emit('start_listen');
        addMessage('System', 'Manual trigger sent...');
    });

    function sendTextCommand() {
        const text = textInput.value.trim();
        if (text) {
            socket.emit('text_command', { text: text });
            textInput.value = '';
        }
    }

    sendBtn.addEventListener('click', sendTextCommand);

    textInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendTextCommand();
        }
    });

    socket.on('connect', () => {
        statusText.textContent = "Connected";
        statusCircle.classList.add('connected');
        addMessage('System', 'Connected to Blueberry Server');
    });

    socket.on('disconnect', () => {
        statusText.textContent = "Disconnected";
        statusCircle.classList.remove('connected');
        addMessage('System', 'Disconnected from server');
    });

    socket.on('message', (data) => {
        addMessage(data.sender, data.text);
    });

    function addMessage(sender, text) {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('message');

        if (sender === 'User') {
            msgDiv.classList.add('user');
        } else if (sender === 'Blueberry') {
            msgDiv.classList.add('blueberry');
        } else {
            msgDiv.classList.add('system');
        }

        const p = document.createElement('p');
        p.textContent = text;
        msgDiv.appendChild(p);

        chatBox.appendChild(msgDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});
