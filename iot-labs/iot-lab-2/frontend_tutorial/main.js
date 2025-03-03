const { app, BrowserWindow } = require("electron");
try {
    require('electron-reloader')(module);
} catch {}
function createWindow() {
    let win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
        }
    });

    win.loadFile("index.html");
}

app.whenReady().then(createWindow);
