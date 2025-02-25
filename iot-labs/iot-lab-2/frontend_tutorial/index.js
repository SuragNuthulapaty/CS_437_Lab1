const net = require('net');

let client = null;
let serverIP = "";
const serverPort = 65432;

function connectToServer() {
    if (client) {
        client.destroy(); // Close any existing connection
    }

    serverIP = document.getElementById("ipAddress").value;
    if (!serverIP) {
        alert("Please enter a valid IP address!");
        return;
    }

    client = new net.Socket();

    client.connect(serverPort, serverIP, () => {
        console.log("✅ Connected to server:", serverIP);
        document.getElementById("status").innerText = "Connected";
        startListening();
    });

    client.on("error", (err) => {
        console.error("❌ Connection error:", err.message);
        document.getElementById("status").innerText = "Connection Failed";
    });

    client.on("close", () => {
        console.warn("❌ Connection closed.");
        document.getElementById("status").innerText = "Disconnected";
    });
}

function startListening() {
    client.on("data", (data) => {
        document.getElementById("distance").innerText = data.toString();
        console.log("📡 Received from server:", data.toString());
    });
}

function sendCommand(command) {
    if (!client || client.destroyed) {
        console.warn("❌ Not connected to server.");
        return;
    }

    client.write(command);
    console.log("📤 Sent:", command);
}
