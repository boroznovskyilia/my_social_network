const createForm = document.getElementById("create-form");
const errorContainer = document.getElementById("error-conrainer");
const errorButton = document.getElementById("error-button")

createForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("access_token");
    const formData = new FormData(createForm);
    try {
        const response = await fetch("/chats/create", {
            method: "POST",
            headers: {
                Authorization: `Bearer ${token}`,
            },
            body: formData,
        });

        if (response.ok) {
            const successStatus = document.createElement("div")
            successStatus.textContent = "Chat was created"
            createForm.appendChild(successStatus)
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