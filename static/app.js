const ws = new WebSocket('ws://localhost:8001/ws');
ws.onmessage = function(event) {
    document.getElementById('accessLog').textContent += event.data + '\n';
};