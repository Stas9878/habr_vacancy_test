from fastapi import FastAPI
import uvicorn
from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserCreate, UserRead
from comics.router import router as comics_router

app = FastAPI()


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(comics_router, prefix='/api')

if __name__ == '__main__':
    uvicorn.run(
        app,
        host='127.0.0.1',
        port=8000    
    )
