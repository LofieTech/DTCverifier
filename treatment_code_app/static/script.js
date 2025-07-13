async function verify() {
    const code = document.getElementById("codeInput").value || document.getElementById("codeSelect").value;
    if (!code) {
        alert("Please select or type a code.");
        return;
    }

    const response = await fetch("/verify", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ code })
    });
    const data = await response.json();
    document.getElementById("result").innerText = data.description;
}

document.getElementById("codeInput").addEventListener("input", async function () {
    const term = this.value;
    if (term.length === 0) {
        document.getElementById("suggestions").innerHTML = "";
        return;
    }

    const res = await fetch(`/search?term=${term}`);
    const results = await res.json();
    const suggestionBox = document.getElementById("suggestions");
    suggestionBox.innerHTML = "";
    results.forEach(item => {
        const li = document.createElement("li");
        li.textContent = `${item.code} - ${item.name}`;
        li.style.cursor = "pointer";
        li.onclick = () => {
            document.getElementById("codeInput").value = item.code;
            suggestionBox.innerHTML = "";
        };
        suggestionBox.appendChild(li);
    });
});
