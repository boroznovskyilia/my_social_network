async function fetchUserChat() {

    const token = localStorage.getItem("access_token");

    const currentURL = window.location.href;
    const urlParts = currentURL.split('/');
    var chatId = null;
    const chatIdIndex = urlParts.indexOf('chats');

    if (chatIdIndex !== -1 && chatIdIndex < urlParts.length - 1) {
        chatId = urlParts[chatIdIndex + 1];
    }

    const response = await fetch(`/chats/${chatId}`, {
        method: "POST", 
        headers: {
            Authorization: `Bearer ${token}`,
        },
        dody:chatId,
    });

    if (!response.ok) {
        errorContainer.style.display = "block"
            errorButton.addEventListener("click",()=>{
                window.location.href = "/login";
                errorContainer.style.display = "none"
            });
    }
    else{
        var ws = new WebSocket(`ws://localhost:8000/chats/${chatId}`)
        const Response = await response.json();
        const data = Response.data;
        // const chat = data.chat
        addUserLink.href = `/chats/${chatId}/add_user`
        addUserLink.addEventListener("click",async(e)=>{
            e.preventDefault()
            await get_auth_add_user(token,chatId)
            window.location.href = `/chats/${chatId}/add_user`
        })

        chatMembersLink.href  = `/chats/${chatId}/members`
        chatMembersLink.addEventListener("click",async(e)=>{
            e.preventDefault()
            await members(token,chatId)
            window.location.href = `/chats/${chatId}/members`
        })
        
        var previous_messages = data.previous_messages
        var user_id = data.user_id
        var user_name = data.user_name
        previous_messages.forEach(message=> {
            displayPrevMessage(message);
        })
       
        ws.onmessage = function(event) {
            const messages = document.getElementById('messages')
            const message = document.createElement('div')
            message.textContent = event.data
            messages.appendChild(message)
           
        };
        sendButton.addEventListener("click" ,(event) =>{
            event.preventDefault()
            var input = document.getElementById("messageText")
            if (input.value.trim() != ''){
                ws.send(JSON.stringify({text:input.value,user_id:user_id,user_name:user_name}))
                input.value = ''
            }
           
        })
        leaveButton.addEventListener("click" ,async() =>{
            await leave(token,chatId)
            window.location.href = `/chats`
        })
        scrollToLatestButton.addEventListener("click", async(event) => {
            event.preventDefault();
            const messagesContainer = document.getElementById("messages_on_page");
            messagesContainer.scrollTop = messagesContainer.scrollHeight
        });
       
    }
        
}

// Call the function to fetch and display posts when the page loads
const errorContainer = document.getElementById("error-conrainer")
const errorButton = document.getElementById("error-button")
const sendButton = document.getElementById("send_button")
const messageInput = document.getElementById("message-input")
const addUserLink = document.getElementById("add_user")
const chatMembersLink = document.getElementById("chat_members")
const leaveButton = document.getElementById("leave")
const scrollToLatestButton = document.getElementById("scroll_to_latest");

window.addEventListener("load",fetchUserChat)   


function displayPrevMessage(message){
    const messageContainer = document.getElementById("prev_message-container")
    const messageElement = document.createElement("div");
    messageElement.textContent = `${message.username}: ${message.text}`
    messageContainer.appendChild(messageElement)
}

async function get_auth_add_user(token,chat_id){
    const response = await fetch(`/chats/${chat_id}/add_user`, {
        method: "GET", 
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
}
async function leave(token,chat_id){
    const response = await fetch(`/chats/${chat_id}/leave`, {
        method: "DELETE", 
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
}

async function members(token,chat_id){
    const response = await fetch(`/chats/${chat_id}/members`,{
        method: "GET", 
        headers: {
            Authorization: `Bearer ${token}`,
        },
    })
}