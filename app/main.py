from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.helpers import APIException
from app.api import auth, permission, role

app = FastAPI()

# Cấu hình cho phép tất cả origin (có thể điều chỉnh lại nếu cần)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hoặc cụ thể ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    # exc.detail là dict đã đúng cấu trúc APIResponse
    return JSONResponse(
        status_code=200,
        content=exc.detail
    )

app.include_router(auth.router)
app.include_router(permission.router)
app.include_router(role.router)


@app.get("/")
def read_root():
    return {"message": "Hello World"}
