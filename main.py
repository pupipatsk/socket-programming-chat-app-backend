from fastapi import FastAPI, Request
from api.routes import user, auth, private_chat, group, websocket
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://socket-programming-chat-app-frontend.onrender.com/"
    ],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(private_chat.router)
app.include_router(group.router)
app.include_router(websocket.router)

# --- Only for demo / testing ---
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def get_chat_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# --- Only for demo / testing ---
