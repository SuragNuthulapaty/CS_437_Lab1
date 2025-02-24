document.querySelector("button").addEventListener("click", () => {
    let input = document.getElementById("myName").value;
    window.electron.sendToServer(input);
});

window.electron.onServerResponse((data) => {
    document.getElementById("greet_from_server").innerText = `Server: ${data}`;
});
