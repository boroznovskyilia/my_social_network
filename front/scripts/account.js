// Function to fetch and display user account data
async function fetchUserAccount() {
    const token = localStorage.getItem("access_token");
   
    const response = await fetch("/account", {
        method: "POST", 
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

    if (!response.ok) {
        // Handle authentication error
        errorContainer.style.display = "block";
        errorButton.addEventListener("click", () => {
            window.location.href = "/login";
            errorContainer.style.display = "none";
        });
    }
    else {
        const data = await response.json();
        const account = data.data;

        const username = document.getElementById("account-username")
        username.textContent = account.username
        username.style.fontSize = "30px"
        const email = document.getElementById("account-email")
        email.textContent = account.email
        email.style.fontSize = "30px"

        const followingContainer = document.getElementById("following-container")
        followingContainer.className = "text-primary"; 
        followingContainer.style.fontSize = "20px"; 
        followingContainer.style.display = "flex"; 
        followingContainer.style.flexDirection = "column";
        if (account.following && account.following.length > 0) {
            account.following.forEach(async (following) => {
                const followingUsername = document.createElement("a");
                followingUsername.className = "mb-2"; 
                followingUsername.style.color = "white"
                followingUsername.textContent = following.username;
                followingUsername.href = `/account/${following.username}`; 
                followingContainer.appendChild(followingUsername);

                followingUsername.addEventListener("click", async () => {
                    await get_auth_user_page(token, following.username);
                });
            });
        } else {
            followingContainer.textContent = "No following.";
        }

        const followersContainer = document.getElementById("followers-container");
        followersContainer.className = "text-primary"; 
        followersContainer.style.fontSize = "20px"; 
        followersContainer.style.display = "flex"; 
        followersContainer.style.flexDirection = "column"; 
        if (account.followers && account.followers.length > 0) {
            account.followers.forEach(async (follower) => {
                const followerUsername = document.createElement("a"); 
                followerUsername.className = "mb-2"; 
                followerUsername.style.color = "white"
                followerUsername.textContent = follower.username;
                followerUsername.href = `/account/${follower.username}`; 
                followersContainer.appendChild(followerUsername);

                followerUsername.addEventListener("click", async () => {
                    await get_auth_user_page(accessToken, follower.username);
                });
            });
        } else {
            followersContainer.textContent = "No followers.";
        }

        // Populate "My Posts" container
        const postsContainer = document.getElementById("posts-container");
        if (account.posts && account.posts.length > 0) {
            account.posts.forEach((post) => {
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
                

                // Create a content element and apply styles
                const postContent = document.createElement("p");
                postContent.textContent = post.content;
                postContent.className = "post-content";
                postContent.style.fontSize = "16px"; 
                postContent.style.color = "#555"; 
                
                // Append title and content to the post div
                postDiv.appendChild(postTitle);
                postDiv.appendChild(postContent);
                postsContainer.appendChild(postDiv);
            });
        } else {
            postsContainer.textContent = "No posts.";
        }
    }
}

// Function to fetch user data on page load
window.addEventListener("load", fetchUserAccount);

// Function to fetch user page data
async function get_auth_user_page(token, username) {
    const response = await fetch(`/account/${username}`, {
        method: "GET",
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
}
    