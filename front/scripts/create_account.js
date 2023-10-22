const createForm = document.getElementById("create-form");
const errorContainer = document.getElementById("error-container");
const errorButton = document.getElementById("error-button")

// Function to handle login form submission
createForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(createForm);
    try {
        const response = await fetch("/create_account", {
            method: "POST",
            body: formData,
        });

        if (response.ok) {
            window.location.href = "/login";
        } else {
            console.error("Create failed");
            createForm.style.display = "none"
            errorContainer.style.display = "block"
            errorButton.addEventListener("click",()=>{
                createForm.style.display = "block"
                errorContainer.style.display = "none"
            })

        }
    } catch (error) {
        console.error("Error:", error);
    }
});