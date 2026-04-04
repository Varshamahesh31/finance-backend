from app.database import engine, SessionLocal
from app.models import Base, User, RoleEnum

Base.metadata.create_all(bind=engine)
db = SessionLocal()
try:
    if not db.query(User).count():
        admin = User(name="Admin", email="admin@test.com", role=RoleEnum.admin)
        db.add(admin)
        db.commit()
        print("Admin user created with ID:", admin.id)
    else:
        print("DB already initialized.")
finally:
    db.close()
