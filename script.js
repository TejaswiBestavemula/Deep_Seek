document.getElementById('sendBtn').addEventListener('click', function () {
    sendMessage();
});

document.getElementById('userInput').addEventListener('keypress', function (event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

function sendMessage() {
    let userMessage = document.getElementById('userInput').value.trim();
    if (!userMessage) return;

    displayMessage(userMessage, 'user');
    document.getElementById('userInput').value = ''; // Clear input field

    fetch('http://127.0.0.1:5000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage })
    })
        .then(response => response.json())
        .then(data => {
            displayMessage(data.reply, 'bot');
        })
        .catch(error => console.error('Error:', error));
}

function displayMessage(message, sender) {
    let chatbox = document.getElementById('chatbox');
    let messageElement = document.createElement('div');
    messageElement.textContent = message;
    messageElement.classList.add(sender);
    chatbox.appendChild(messageElement);
    chatbox.scrollTop = chatbox.scrollHeight; // Auto-scroll
}
