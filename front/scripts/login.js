const loginForm = document.getElementById("login-form");
const logoutContainer = document.getElementById("logout-container");
const usernameDisplay = document.getElementById("username-display");
const logoutButton = document.getElementById("logout-button");
const errorContainer = document.getElementById("error-container");
const errorButton = document.getElementById("error-button")

// Function to handle login form submission
loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(loginForm);


    // Send a POST request to your API for authentication
    try {
        const response = await fetch("/login", {
            method: "POST",
            body: formData,
        });

        if (response.ok) {
            // const Response = await response.json()
            // const status = Response.status
            // const data = Response.data;
            const data = await response.json()
           
            const accessToken = data.access_token;
            localStorage.setItem("access_token", accessToken);
            await get_auth_posts(accessToken);
            await get_auth_account(accessToken);
            await get_auth_create_posts(accessToken);
            window.location.href = "/posts";
        }   
        else {
            console.error("Authentication failed");
            loginForm.style.display = "none"
            errorContainer.style.display = "block"
            errorButton.addEventListener("click",()=>{
                loginForm.style.display = "block"
                errorContainer.style.display = "none"
            })
        }

    } catch (error) {
        console.error("Error:", error);
    }
});

// Function to handle logout
logoutButton.addEventListener("click", async() => {
    const response = await fetch("/logout",{
        method:"POST",
        headers: {
            Authorization: `Bearer ${token}`,
        },
    })
    localStorage.removeItem("access_token");
});
async function get_auth_posts(token){
    const response = await fetch("/posts", {
        method: "GET",
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
}
async function get_auth_account(token){
    const response = await fetch("/account", {
        method: "GET",
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
}
async function get_auth_create_posts(token){
    const response = await fetch("/create_post", {
        method: "GET",
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
}

