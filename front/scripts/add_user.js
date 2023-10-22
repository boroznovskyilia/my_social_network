const createForm = document.getElementById("create-form");
const errorContainer = document.getElementById("error-conrainer");
const errorButton = document.getElementById("error-button")

createForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("access_token");

    const currentURL = window.location.href;
    const urlParts = currentURL.split('/');
    var chat_id = null;
    const chat_idIndex = urlParts.indexOf('chats');

    if (chat_idIndex !== -1 && chat_idIndex < urlParts.length - 1) {
        chat_id = urlParts[chat_idIndex + 1];
    }

    const formData = new FormData(createForm);
   
    try {
        const response = await fetch(`/chats/${chat_id}/add_user`, {
            method: "POST",
            headers: {
                Authorization: `Bearer ${token}`,
            },
            body: formData,
        });

        if (response.ok) {
            const successStatus = document.createElement("div")
            successStatus.textContent = "user was added"
            createForm.appendChild(successStatus)
        } else {
            // console.error("Create failed");
            const errorResponse = await response.json();
            console.error("Error response:", errorResponse);
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