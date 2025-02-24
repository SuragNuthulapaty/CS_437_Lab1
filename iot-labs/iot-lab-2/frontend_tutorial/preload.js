const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("electron", {
    sendToServer: (message) => ipcRenderer.send("send-to-server", message),
    onServerResponse: (callback) => ipcRenderer.on("server-response", (event, data) => callback(data)),
});
