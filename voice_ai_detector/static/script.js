const audioInput = document.getElementById('audio-input');
const dropZone = document.getElementById('drop-zone');

audioInput.addEventListener('change', (e) => handleUpload(e.target.files[0]));

async function handleUpload(file) {
    if (!file) return;

    // Show Loader
    document.getElementById('drop-zone').classList.add('hidden');
    document.getElementById('loader').classList.remove('hidden');

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/detect', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        showResult(data);
    } catch (error) {
        alert("Error analyzing file");
        resetUI();
    }
}

function showResult(data) {
    document.getElementById('loader').classList.add('hidden');
    document.getElementById('result-card').classList.remove('hidden');
    
    const isAI = data.prediction === "AI_GENERATED";
    const resultText = document.getElementById('result-text');
    const scoreVal = document.getElementById('score-value');
    const fill = document.getElementById('progress-fill');

    resultText.innerText = isAI ? "AI Generated" : "Human Voice";
    resultText.style.color = isAI ? "#f87171" : "#4ade80";
    
    scoreVal.innerText = data.confidence;
    
    // Trigger progress bar animation
    setTimeout(() => {
        fill.style.width = (data.confidence * 100) + "%";
        fill.style.backgroundColor = isAI ? "#f87171" : "#4ade80";
    }, 100);
}

function resetUI() {
    location.reload();
}
