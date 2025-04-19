from fastapi import FastAPI, Request
from api.routes import user, auth, private_chat, group, websocket
from fastapi.templating import Jinja2Templates

app = FastAPI()

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