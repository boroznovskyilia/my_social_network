async function fetchChatUsers() {
    const token = localStorage.getItem("access_token");
    const currentURL = window.location.href;
    const urlParts = currentURL.split('/');
    var chatId = null;
    const chatIdIndex = urlParts.indexOf('chats');

    if (chatIdIndex !== -1 && chatIdIndex < urlParts.length - 1) {
        chatId = urlParts[chatIdIndex + 1];
    }
    const response = await fetch(`/chats/${chatId}/members`, {
        method: "POST", 
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

    if (!response.ok) {
        errorContainer.style.display = "block";
        errorButton.addEventListener("click", () => {
            window.location.href = "/login";
            errorContainer.style.display = "none";
        });
    } else {
        const Response = await response.json();
        const data = Response.data;
        const membersContainer = document.getElementById("members-container");
        if (data.users && data.users.length > 0) {
            data.users.forEach((user) => {
                const userContainer = document.createElement("div");
                userContainer.classList.add("user-container");
                userContainer.textContent = user;
                membersContainer.appendChild(userContainer);
            });
        } else {
            // Handle the case where there are no users to display
            membersContainer.textContent = "No users available.";
        }
    }
}

// Call the function to fetch and display members when the page loads
const errorContainer = document.getElementById("error-container");  
const errorButton = document.getElementById("error-button");
window.addEventListener("load", fetchChatUsers);
