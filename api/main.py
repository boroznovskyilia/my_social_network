from fastapi.staticfiles import StaticFiles
import uvicorn
from fastapi import FastAPI
from auth.router import router as auth_router
from user.router import router as user_router
from posts.router import router as posts_router
from chat.router import router as chat_router
from template_routers.router import router as show_router

app = FastAPI()
app.mount("/scripts", StaticFiles(directory="front/scripts"), name="scripts")
app.mount("/static",StaticFiles(directory="front/static"),name = "static")

app.include_router(auth_router)
app.include_router(user_router) 
app.include_router(posts_router)
app.include_router(chat_router) 
app.include_router(show_router)
        
if __name__ == "__main__":
    uvicorn.run("main:app",reload=True) 
    # uvicorn.run(app)