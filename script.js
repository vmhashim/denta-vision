function processImage() {
    let fileInput = document.getElementById('upload');
    let file = fileInput.files[0];
    
    if (!file) {
        alert("Please upload an image first.");
        return;
    }

    let reader = new FileReader();
    reader.onload = function(event) {
        let imgElement = document.createElement("img");
        imgElement.src = event.target.result;
        imgElement.onload = function() {
            // Image processing logic (if any)
            // Since we don't have Python, this is a placeholder
            // For actual age estimation, you might need to send the image
            // to a backend server or use a JS library for image processing

            let estimatedAge = Math.floor(Math.random() * 60) + 20; // Mock result
            document.getElementById('result').innerText = `Estimated Age: ${estimatedAge} years`;
        }
    };
    reader.readAsDataURL(file);
}
