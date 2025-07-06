# FastAPI Project

This project uses FastAPI with a standard folder structure:

- `app/` - Main application code
  - `api/` - API route definitions
  - `core/` - Core settings and utilities
  - `models/` - Database models
  - `schemas/` - Pydantic schemas
  - `services/` - Business logic
  - `db/` - Database connection and utilities
  - `tests/` - Test cases
- `main.py` - FastAPI entry point

## Getting Started

1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Run database migration (sử dụng Alembic):
   ```sh
   pip install alembic python-dotenv
   # Khởi tạo Alembic nếu chưa có
   alembic init alembic
   # Sau đó tạo migration và upgrade như bình thường:
   alembic revision --autogenerate -m "Tên migration"
   alembic upgrade head
   # Hạ cấp database về phiên bản trước
   alembic downgrade -1
   # Xem lịch sử migration
   alembic history
   # Kiểm tra trạng thái migration hiện tại
   alembic current
   # Chạy migration tới một version cụ thể
   alembic upgrade <version>
   # Hạ cấp về một version cụ thể
   alembic downgrade <version>
   ```
3. Run the app:
   ```sh
   uvicorn app.main:app --reload
   ```

> **Lưu ý:** Để Alembic tự động nhận diện các bảng khi migration, bạn phải import tất cả các model vào file `alembic/env.py` (thường là `from app.models import *`). Nếu không, Alembic sẽ không tạo hoặc cập nhật bảng tương ứng trong database.
