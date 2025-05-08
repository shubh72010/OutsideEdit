document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('upload-form');
    const imageInput = document.getElementById('image-input');
    const loadingIndicator = document.getElementById('loading');

    form.addEventListener('submit', function (e) {
        if (imageInput.files.length === 0) {
            e.preventDefault();
            alert('Please select an image file to upload.');
            return;
        }

        // Show loading indicator
        loadingIndicator.style.display = 'block';
    });
});