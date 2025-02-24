// Attach event listener to the submit button
document.querySelector("button").addEventListener("click", () => {
    let input = document.getElementById("myName").value;
    window.electron.sendToServer(input); // Send message to backend
});

// Listen for server responses
window.electron.onServerResponse((data) => {
    document.getElementById("greet_from_server").innerText = `Server: ${data}`;
});
