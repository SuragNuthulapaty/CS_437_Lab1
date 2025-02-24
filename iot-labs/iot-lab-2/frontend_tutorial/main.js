const { app, BrowserWindow, ipcMain } = require("electron");
const net = require("net");

let mainWindow;
const SERVER_HOST = "10.195.7.214";
const SERVER_PORT = 65432;

app.whenReady().then(() => {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: __dirname + "/preload.js",
        },
    });

    mainWindow.loadFile("index.html");
});

// Handle frontend request
ipcMain.on("send-to-server", (event, message) => {
    const client = new net.Socket();

    client.connect(SERVER_PORT, SERVER_HOST, () => {
        console.log("Connected to server, sending message...");
        client.write(message + "\r\n");  // Send message
    });

    client.on("data", (data) => {
        console.log("Received from server: " + data.toString());
        event.reply("server-response", data.toString());  // Send data back to frontend
        client.destroy();
    });

    client.on("error", (err) => {
        console.error("Connection error:", err.message);
        event.reply("server-response", "Error connecting to server");
    });

    client.on("close", () => {
        console.log("Connection closed");
    });
});
