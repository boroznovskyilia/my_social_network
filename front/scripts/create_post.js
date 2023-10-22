const createForm = document.getElementById("create-form");
const errorContainer = document.getElementById("error-conrainer");
const errorButton = document.getElementById("error-button")

// Function to handle login form submission
createForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(createForm);
    try {
        const token = localStorage.getItem("access_token");
        const response = await fetch("/create_post", {
            method: "POST",
            headers: {
                Authorization: `Bearer ${token}`,
            },
            body: formData,
        });

        if (response.ok) {
            const successStatus = document.getElementById("success-container")
            successStatus.style.display = "block"
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