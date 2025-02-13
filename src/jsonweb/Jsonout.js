function highlightJson(json) {
    const jsonString = JSON.stringify(json, null, 4);
    return jsonString
        .replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(\.\d*)?([eE][+-]?\d+)?/g, (match) => {
            let cls = 'json-value';
            if (/^"/.test(match)) {
                if (/:$/.test(match)) {
                    cls = 'json-key';
                } else {
                    cls = 'json-string';
                }
            } else if (/true|false/.test(match)) {
                cls = 'json-boolean';
            } else if (/null/.test(match)) {
                cls = 'json-null';
            } else if (/^-?\d+(\.\d*)?([eE][+-]?\d+)?$/.test(match)) {
                cls = 'json-number';
            }
            return `<span class="${cls}">${match}</span>`;
        })
        .replace(/[{}[\],]/g, (match) => `<span class="json-bracket">${match}</span>`);
}

function openJsonPopup(jsonData, title) {
    let parsedJson;
    try {
        parsedJson = typeof jsonData === "string" ? JSON.parse(jsonData) : jsonData;
    } catch (error) {
        console.error("Invalid JSON data:", error);
        document.getElementById("popup-content").innerHTML = `<p class="error">Error: Invalid JSON data</p>`;
        return;
    }

    const formattedJson = highlightJson(parsedJson);
    
    document.getElementById("popup-content").innerHTML = `
        <div class="json-container">
            <h2>${title}</h2>
            <pre class="json-display">${formattedJson}</pre>
        </div>`;
    
    document.getElementById("popup-overlay").style.display = "block";
    document.getElementById("popup").style.display = "block";
}

function closeJsonPopup() {
    document.getElementById("popup-overlay").style.display = "none";
    document.getElementById("popup").style.display = "none";
}
