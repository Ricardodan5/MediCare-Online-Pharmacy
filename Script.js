// Select the HTML elements
const prescriptionForm = document.getElementById("prescriptionForm");
const prescriptionInput = document.getElementById("prescription");
const fileName = document.getElementById("fileName");
const message = document.getElementById("message");

// Display the selected filename
prescriptionInput.addEventListener("change", function () {

    const file = prescriptionInput.files[0];

    if (!file) {
        fileName.textContent = "No file selected.";
        return;
    }

    const allowedTypes = [
        "application/pdf",
        "image/jpeg",
        "image/png"
    ];

    const maxSize = 10 * 1024 * 1024; // 10 MB

    if (!allowedTypes.includes(file.type)) {
        fileName.textContent = "Invalid file type.";
        prescriptionInput.value = "";
        return;
    }

    if (file.size > maxSize) {
        fileName.textContent = "File is too large. Maximum size is 10 MB.";
        prescriptionInput.value = "";
        return;
    }

    fileName.textContent = "Selected: " + file.name;
    message.textContent = "";
});

// Handle form submission
prescriptionForm.addEventListener("submit", function (event) {

    event.preventDefault();

    const file = prescriptionInput.files[0];

    if (!file) {
        message.textContent = "Please select your prescription.";
        return;
    }

    message.textContent =
        "Demo successful! Your file passed the basic checks. " +
        "No prescription has been uploaded or sent for verification.";

    message.style.color = "#087c59";

    console.log("Selected prescription:", file.name);
});
