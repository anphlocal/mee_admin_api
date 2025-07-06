from app.db.database import SessionLocal

class DBSession:
    def __init__(self):
        self.db = None

    def __enter__(self):
        self.db = SessionLocal()
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.db:
            self.db.close()

    @staticmethod
    def dependency():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
