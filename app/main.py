from fastapi import FastAPI
from app.api import auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Cấu hình cho phép tất cả origin (có thể điều chỉnh lại nếu cần)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hoặc cụ thể ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Hello World"}
