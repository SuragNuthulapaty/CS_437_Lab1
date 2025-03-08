const net = require('net');

let client = null;
let serverIP = "10.195.7.214";
const serverPort = 65432;

let data_points = [];

let distanceChart = new Chart(document.getElementById("distanceChart"), {
    type: 'line',
    options: '',
    data: {
        labels: [],
        datasets: [{ label: 'Distance (cm)', data: [], borderColor: 'blue', fill: false }]
    }
});


let connected = true;

function toggleConnection() {
    const button = document.getElementById("connect-button");
    document.querySelector("main").classList.toggle("hidden");

    if (connected) {
        button.innerText = "Connect";
        disconnectFromServer();
    } else {
        connected = true;
        button.innerText = "Disconnect";
        connectToServer();
    }
}

const slider_0 = document.getElementById("slider_0");
const angleDisplay_0 = document.getElementById("angleValue_0");

noUiSlider.create(slider_0, {
    start: 90,
    range: {
        min: 50,
        max: 130
    },
    step: 1,
    connect: [true, false]
});

slider_0.noUiSlider.on("update", function (values) {
    const angle = Math.round(values[0]);
    angleDisplay_0.textContent = angle;

    let v = "0 " + angle

    sendCommand(v);
});

function connectToServer() {
    if (client) {
        client.destroy();
    }

    if (document.getElementById("ipAddress")) {
        serverIP = document.getElementById("ipAddress").value;
        console.log(`Now using ${serverIP}`);
    }


    if (!serverIP) {
        alert("Please enter a valid IP address!");
        return;
    }

    client = new net.Socket();

    client.connect(serverPort, serverIP, () => {
        console.log("Connected to server:", serverIP);
        // document.getElementById("status").innerText = "Connected";
        startListening();
    });

    client.on("error", (err) => {
        console.error("Connection error:", err.message);
        document.getElementById("status").innerText = "Connection Failed";
    });

    client.on("close", () => {
        console.warn("Connection closed.");
        document.getElementById("status").innerText = "Disconnected";
    });
}

function disconnectFromServer() {
    if (client) {
        console.log("ajkhdfxgchj")
        client.destroy()

        distanceChart.destroy()
        distanceChart = new Chart(document.getElementById("distanceChart"), {
            type: 'line',
            options: '',
            data: {
                labels: [],
                datasets: [{ label: 'Distance (cm)', data: [], borderColor: 'blue', fill: false }]
            }
        });

        data_points = []
        distanceChart.data.labels = [];
        distanceChart.data.datasets.forEach(dataset => {
            dataset.data = [];
        });
    }
}

function startListening() {
    client.on("data", (data) => {
        try {
            const jsonData = JSON.parse(data.toString());

            // Update displayed direction
            console.log(jsonData.direction);
            if (jsonData.direction == "0") {
                document.getElementById("direction").innerText = "Bot is not moving"
            } else {
                document.getElementById("direction").innerText = "Bot is moving"
            }

            // Update charts
            // updateChart(distanceChart, distanceData, jsonData.distance);

            let max_v = 100

            const np = {data: jsonData.distance, time: new Date().toLocaleTimeString()}
            data_points.push(np);

            if (distanceChart.data.labels.length > max_v) {
                data_points.shift();
            }

            distanceChart.data.labels = data_points.map(d => d.time);
            distanceChart.data.datasets[0].data = data_points.map(d => d.data);

            distanceChart.update();

            // console.log("Received from server:", jsonData);

            // const img = document.getElementById("cameraStream");
            // img.src = `data:image/jpeg;base64,${jsonData.img}`;

        } catch (error) {
            console.error("Error parsing JSON:", error);
        }
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

document.addEventListener("keyup", function (event) {
    let stopCommand = "s";

    switch (event.key) {
        case "ArrowUp":
        case "ArrowDown":
        case "ArrowLeft":
        case "ArrowRight":
            sendCommand(stopCommand);
            break;
    }
});

function sendCommand(command) {
    if (!client || client.destroyed) {
        console.warn("Not connected to server.");
        return;
    }

    client.write(command);
    console.log("Sent:", command);
}
