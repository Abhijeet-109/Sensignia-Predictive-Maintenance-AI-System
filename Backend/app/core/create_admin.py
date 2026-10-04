from getpass import getpass

from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.database.connection import SessionLocal
from app.models.user import User


def create_admin():
    db: Session = SessionLocal()

    try:
        username = input("Admin username: ").strip()
        email = input("Admin email: ").strip()
        password = getpass("Admin password: ")

        if not username or not email or not password:
            print("All fields are required.")
            return

        existing_user = (
            db.query(User)
            .filter(
                (User.username == username)
                | (User.email == email)
            )
            .first()
        )

        if existing_user:
            print("A user with this username or email already exists.")
            return

        admin = User(
            username=username,
            email=email,
            hashed_password=hash_password(password),
            role="admin",
            is_active=True,
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

        print()
        print("Initial admin created successfully.")
        print(f"Admin ID: {admin.id}")
        print(f"Username: {admin.username}")
        print(f"Role: {admin.role}")

    finally:
        db.close()


if __name__ == "__main__":
    create_admin()