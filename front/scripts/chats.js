const chatsContainer = document.getElementById("chats-container");
const errorContainer = document.getElementById("error-container");
const errorButton = document.getElementById("error-button");

// Function to fetch and display user's chats
async function fetchUserChats() {
    const token = localStorage.getItem("access_token");

    const response = await fetch("/chats", {
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
        const data = await response.json();
        const token = localStorage.getItem("access_token");

        // Create link to the "Create Chat" page
        const createChatLink = document.createElement("a");
        createChatLink.href = "/chats/create";
        createChatLink.textContent = "Create Chat";
        createChatLink.classList.add("btn", "btn-primary");
        createChatLink.addEventListener("click", async () => {
            await getAuthCreateChat(token);
            window.location.href = "/chats/create";
        });

        if (data.data && data.data.length > 0) {
            data.data.forEach((chat) => {
                // Create a link for each chat
                const chatLink = document.createElement("a");
                chatLink.href = `/chats/${chat.id}`;
                chatLink.textContent = chat.name;
                chatLink.classList.add("btn", "btn-light", "mb-3", "d-block");
                chatLink.addEventListener("click", async () => {
                    await getAuthChat(token, chat.id);
                    window.location.href = `/chats/${chat.id}`;
                });

                // Append the chat link to the chats container
                chatsContainer.appendChild(chatLink);
            });
        } else {
            // Handle the case where there are no chats to display
            chatsContainer.textContent = "No chats available.";
        }
    }
}

// Function to fetch chat data with authentication
async function getAuthChat(token, id) {
    const response = await fetch(`/chats/${id}`, {
        method: "GET",
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
}

// Function to fetch chat creation page with authentication
async function getAuthCreateChat(token) {
    const response = await fetch("/chats/create", {
        method: "GET",
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
}

// Load user chats when the page loads
window.addEventListener("load", fetchUserChats);
