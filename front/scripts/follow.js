async function fetchUserFollow_page() {
    const followForm = document.getElementById("follow-form")
    const errorContainer = document.getElementById("error-container")
    const errorButton = document.getElementById("error-button")
    const successFollow = document.getElementById("success-follow")
    const successUnfollow = document.getElementById("success-unfollow")
    const followButton = document.getElementById("follow_button")
    const unfollowButton = document.getElementById("unfollow_button")


    followButton.addEventListener("click",async(e)=>{
        e.preventDefault();
        const formData = new FormData(followForm);
        const usernmae = formData.get("username")
        const token = localStorage.getItem("access_token");
    
        const response = await fetch("/follow", {
            method: "POST",
            headers: {
                Authorization: `Bearer ${token}`,
            },
            body: formData,
        });
        if(response.ok){
            followForm.style.display = "none"
            successFollow.style.display = "block"
        }
        else{
            console.error("Create failed")
            followForm.style.display = "none"
            errorContainer.style.display = "block"
            errorButton.addEventListener("click",()=>{
                followForm.style.display = "block"
                errorContainer.style.display = "none"
            })
        }
        
    });
    unfollowButton.addEventListener("click",async(e)=>{
        e.preventDefault();
        const formData = new FormData(followForm);
        const token = localStorage.getItem("access_token");
        try {
            const response = await fetch("/unfollow", {
                method: "POST",
                headers: {
                    Authorization: `Bearer ${token}`,
                },
                body: formData,
            });
            if(response.ok){
                followForm.style.display = "none"
                successUnfollow.style.display = "block"
            }
            else{
                console.error("Create failed")
                followForm.style.display = "none"
                errorContainer.style.display = "block"
                errorButton.addEventListener("click",()=>{
                followForm.style.display = "block"
                errorContainer.style.display = "none"
            })
            }
        } catch (error) {
            console.error("Error:", error);
        }
    });
}

window.addEventListener("load",fetchUserFollow_page)