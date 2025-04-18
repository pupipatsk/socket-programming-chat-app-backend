from fastapi import FastAPI
from api.routes import user, auth, private_chat, group

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(private_chat.router)
app.include_router(group.router)