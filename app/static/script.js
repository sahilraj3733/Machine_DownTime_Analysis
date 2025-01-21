
document.getElementById('uploadForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', document.getElementById('fileInput').files[0]);

    const response = await fetch('/upload', {
        method: 'POST',
        body: formData,
    });

    const result = await response.json();
    document.getElementById('uploadStatus').textContent = result.message;
});

document.addEventListener('DOMContentLoaded', function () {
    
    const trainButton = document.getElementById('trainButton');
    const trainStatusElement = document.getElementById('trainStatus');
    const accuracyElement = document.getElementById('accuracy');
    const f1ScoreElement = document.getElementById('f1Score');

    if (!trainButton || !trainStatusElement || !accuracyElement || !f1ScoreElement) {
        console.error("One or more elements not found.");
        return;
    }

    trainButton.addEventListener('click', function() {
        trainStatusElement.textContent = "Training in progress... Please wait.";

        
        fetch('/train', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.Accuracy && data['F1-Score']) {
                // Update the displayed accuracy and F1-score
                accuracyElement.textContent = data.Accuracy.toFixed(4); 
                f1ScoreElement.textContent = data['F1-Score'].toFixed(4); 

                // Update the status message
                trainStatusElement.textContent = "Model trained successfully!";
            } else {
                trainStatusElement.textContent = "Error: Could not retrieve model performance data.";
            }
        })
        .catch(error => {
            trainStatusElement.textContent = "Error: " + error.message;
        });
    });
});


document.getElementById('predictForm').addEventListener('submit', function(event) {
    event.preventDefault(); 

    const jsonInput = document.getElementById('jsonInput').value;

   
    let parsedData;
    try {
        parsedData = JSON.parse(jsonInput);
    } catch (error) {
        document.getElementById('predictionResult').textContent = 'Invalid JSON format!';
        return;
    }

    // Make a POST request to the /predict route
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(parsedData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.Downtime) {
            // Show prediction result
            document.getElementById('predictionResult').textContent = `Prediction: ${data.Downtime} with Confidence: ${data.Confidence}`;
        } else {
            document.getElementById('predictionResult').textContent = 'Error: ' + data.message;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('predictionResult').textContent = 'Error making prediction';
    });
});
