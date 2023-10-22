from fastapi.templating import Jinja2Templates
from fastapi import Depends,Request,Form,APIRouter
from auth.utils import get_current_active_user, get_db
from chat.service import ChatService

templates = Jinja2Templates(directory="front/templates")

router = APIRouter()

@router.get("/",tags=['show'])
async def main(request:Request):
    return templates.TemplateResponse("index.html",{"request":request})

@router.get("/login",tags=['show'])
async def login_page(request:Request):
    return templates.TemplateResponse("login.html",{"request":request})

@router.get("/posts",tags=['show'])
async def show_posts(request: Request):
    return templates.TemplateResponse("posts.html", {"request": request})

@router.get("/create_post",tags=["show"])
async def create_post(request:Request):
    return templates.TemplateResponse("create_post.html",{"request":request})

@router.get("/create_account",tags = ["show"])
async def create_account(request:Request):
    return templates.TemplateResponse("create_account.html",{"request":request})

@router.get("/account",tags=['show'])
async def show_account(request:Request):
    return templates.TemplateResponse("account.html",{"request":request})

@router.get("/chats",tags=['show'])
async def show_chats(request:Request):
    return templates.TemplateResponse("chats.html",{"request":request})

@router.get("/chats/create",tags = ['show'])
async def create_chat(request:Request):
    return templates.TemplateResponse("create_chat.html",{"request":request})

@router.get("/chats/{chat_id}",tags=['show'])
async def show_chat(request:Request,chat_id:int,db = Depends(get_db)):
    chat = await ChatService().get_chat(db,chat_id)
    return templates.TemplateResponse("chat.html",{"request":request,"chat_id":chat_id,"chat_name":chat.name})

@router.get("/chats/{chat_id}/add_user")    
async def add_user(request:Request):
    return templates.TemplateResponse("add_user.html",{"request":request})

@router.get("/chats/{chat_id}/members")
async def members(request:Request):
    return templates.TemplateResponse("chat_members.html",{"request":request})


@router.get("/following_page")
async def following_page(request:Request):
    return templates.TemplateResponse("follow.html",{"request":request})

@router.get("/account/{username}")
async def get_user_account(request:Request,username:str):
    return templates.TemplateResponse("user_account.html",{"request":request,"username":username})

