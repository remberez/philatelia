import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from users.api import router as user_router
from groups.api import router as groups_router
from posts.api import router as posts_router
from comment.api import router as comments_router

app = FastAPI()
app.include_router(router=user_router)
app.include_router(router=groups_router)
app.include_router(router=posts_router)
app.include_router(router=comments_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins="http://localhost:5173",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run("main:app")
