const net = require('net');

let client = null;
let serverIP = "";
const serverPort = 65432;

// Chart.js data
const distanceData = [];
const speedData = [];
const batteryData = [];

// Create charts
const distanceChart = new Chart(document.getElementById("distanceChart"), {
    type: 'line',
    data: {
        labels: [],
        datasets: [{ label: 'Distance (cm)', data: distanceData, borderColor: 'blue', fill: false }]
    }
});

const speedChart = new Chart(document.getElementById("speedChart"), {
    type: 'line',
    data: {
        labels: [],
        datasets: [{ label: 'Speed (m/s)', data: speedData, borderColor: 'green', fill: false }]
    }
});

const batteryChart = new Chart(document.getElementById("batteryChart"), {
    type: 'line',
    data: {
        labels: [],
        datasets: [{ label: 'Battery (%)', data: batteryData, borderColor: 'red', fill: false }]
    }
});

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
        try {
            const jsonData = JSON.parse(data.toString());

            // Update displayed direction
            document.getElementById("direction").innerText = jsonData.direction;

            // Update charts
            updateChart(distanceChart, distanceData, jsonData.distance);
            updateChart(speedChart, speedData, jsonData.speed);
            updateChart(batteryChart, batteryData, jsonData.battery);

            console.log("📡 Received from server:", jsonData);
        } catch (error) {
            console.error("❌ Error parsing JSON:", error);
        }
    });
}

function updateChart(chart, dataset, newValue) {
    dataset.push(newValue);
    if (dataset.length > 10) dataset.shift(); // Keep only last 10 values
    chart.data.labels.push(new Date().toLocaleTimeString());
    if (chart.data.labels.length > 10) chart.data.labels.shift();
    chart.update();
}

function sendCommand(command) {
    if (!client || client.destroyed) {
        console.warn("❌ Not connected to server.");
        return;
    }

    client.write(command);
    console.log("📤 Sent:", command);
}
