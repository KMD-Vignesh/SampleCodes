function highlightJson(json) {
    const  = JSON.stringify(json, null, 4);
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

function openPopupJson(fileName, test_case_name) {
    const popupContent = document.getElementById("popup-content");
    const formatted_json = highlightJson(fileName);
    popupContent.innerHTML = `
        <div class="json-container">
            <h1>${test_case_name}</h1>
            <pre id="${test_case_name}-json-content">${formatted_json}</pre>
        </div>`;
    document.getElementById("popup-overlay").style.display = "block";
    document.getElementById("popup").style.display = "block";
    document.getElementById("close-popup").classList.remove("hidden");
}
