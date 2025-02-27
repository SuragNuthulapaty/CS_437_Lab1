const net = require('net');

let client = null;
let serverIP = "";
const serverPort = 65432;

const distanceData = [];

const distanceChart = new Chart(document.getElementById("distanceChart"), {
    type: 'line',
    data: {
        labels: [],
        datasets: [{ label: 'Distance (cm)', data: distanceData, borderColor: 'blue', fill: false }]
    }
});


function connectToServer() {
    if (client) {
        client.destroy();
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

function disconnectFromServer() {
    if (client) {
        client.destroy()

        distanceData = []
    }
}

function startListening() {
    client.on("data", (data) => {
        try {
            const jsonData = JSON.parse(data.toString());

            // Update displayed direction
            document.getElementById("direction").innerText = jsonData.direction;

            // Update charts
            // updateChart(distanceChart, distanceData, jsonData.distance);

            let max_v = 100
            distanceData.push(jsonData.distance);
            distanceChart.data.labels.push(new Date().toLocaleTimeString());

            console.log(distanceData.length, "before")

            if (distanceChart.data.labels.length > max_v) {
                distanceData.shift();
                distanceChart.data.labels.shift();
            }

            console.log(distanceData.length, "after. added", jsonData.distance)

            distanceChart.update();

            console.log("Received from server:", jsonData);
        } catch (error) {
            console.error("Error parsing JSON:", error);
        }
    });

    client.on("camera-frame", (event, base64Image) => {
        const img = document.getElementById("cameraStream");
        img.src = `data:image/jpeg;base64,${base64Image}`;
    });
}

function updateChart(chart, dataset, newValue) {
    let max_v = 100
    dataset.push(newValue);
    chart.data.labels.push(new Date().toLocaleTimeString());

    console.log(dataset.length, "before")

    if (chart.data.labels.length > max_v) {
        dataset.shift();
        chart.data.labels.shift();
    }

    console.log(dataset.length, "after. added", newValue)

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
