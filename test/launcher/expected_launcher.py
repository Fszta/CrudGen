import uvicorn
from fastapi import FastAPI
from database.db_init import Base, engine
from router import table_1_router, table_2_router
from starlette.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(table_1_router.router)
app.include_router(table_2_router.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0",port=8080)
