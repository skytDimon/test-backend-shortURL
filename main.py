import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from src.short_URL import shorten_url
from fastapi import FastAPI, Depends, APIRouter
from src.auth.base_config import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate

templates = Jinja2Templates(directory="templates")

app = FastAPI(
    title="ShortURL"
)


# app.mount("/", StaticFiles(directory="src/index.html", html=True))
@app.get("/", tags=["Front"])
def get_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="",
    tags=["Auth"],
)


@app.get("/shortURL", tags=["Generate"])
def get_shortedURL(url: str):
    return f"Ваша сокращенная ссылка -> {shorten_url(url=url)}"


if __name__ == "__main__":
    uvicorn.run("main:app --reload", port=5000, log_level="info")
