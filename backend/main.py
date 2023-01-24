from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from domain.generator import generator_router

app = FastAPI()

origins = [
    "http://127.0.0.1:5173",  # 또는 "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}

app.include_router(generator_router.router)
