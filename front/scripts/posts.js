async function fetchUserPosts() {
    const token = localStorage.getItem("access_token");
   
    const response = await fetch("/posts", {
        method: "POST", 
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

    if (!response.ok) {
        errorContainer.style.display = "block"
            errorButton.addEventListener("click",()=>{
                window.location.href = "/login";
                errorContainer.style.display = "none"
            });
    }
    else{
        const Response = await response.json();
        const data = Response.data
        const postsContainer = document.getElementById("posts-container");
        if (data && data.length > 0) {
            data.forEach((post) => {
                // Create a div for each post
                const postDiv = document.createElement("div");
                postDiv.className = "post";
                postDiv.style.backgroundColor = "#f2f2f2"; 
                postDiv.style.width = "100%";
                postDiv.style.padding = "10px"; 
                
                // Create a title element and apply styles
                const postTitle = document.createElement("h2");
                postTitle.textContent = post.article;
                postTitle.className = "post-title";
                postTitle.style.fontSize = "28px"; 
                postTitle.style.fontWeight = "bold"; 
                postTitle.style.color = "#333";
                
                const postAuthor = document.createElement("h4");
                postAuthor.textContent = post.username;
                postAuthor.className = "post-author";
                postAuthor.style.fontSize = "14px"; 
                postAuthor.style.fontWeight = "bold"; 
                postAuthor.style.color = "#333";

                // Create a content element and apply styles
                const postContent = document.createElement("p");
                postContent.textContent = post.content;
                postContent.className = "post-content";
                postContent.style.fontSize = "16px"; 
                postContent.style.color = "#555"; 
                
                // Append title and content to the post div
                postDiv.appendChild(postTitle);
                postDiv.appendChild(postAuthor)
                postDiv.appendChild(postContent);
                postsContainer.appendChild(postDiv);
            });
        } else {
            // Handle the case where there are no posts to display
            postsContainer.textContent = "No posts available.";
        }
    }
}

// Call the function to fetch and display posts when the page loads
const errorContainer = document.getElementById("error-conrainer");  
const errorButton = document.getElementById("error-button")
const showButton = document.getElementById("show-button")
const followLink = document.getElementById("follow-page")
const chatsLink = document.getElementById("chat-page")
window.addEventListener("load",fetchUserPosts)

followLink.addEventListener("click",async()=>{
    const token = localStorage.getItem("access_token");
    await get_auth_follow_page(token);
    window.location.href = "/following_page";
});

chatsLink.addEventListener("click",async()=>{
    const token = localStorage.getItem("access_token");
    await get_auth_chats(token);
    window.location.href = "/chats";
});

async function get_auth_follow_page(token){
    const response = await fetch("/following_page", {
        method: "GET",
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
}
async function get_auth_chats(token){
    const response = await fetch("/chats", {
        method: "GET",
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
}