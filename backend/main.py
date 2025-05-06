import uvicorn
from fastapi import FastAPI
from users.api import router as user_router
from groups.api import router as groups_router

app = FastAPI()
app.include_router(router=user_router)
app.include_router(router=groups_router)

if __name__ == '__main__':
    uvicorn.run("main:app")
