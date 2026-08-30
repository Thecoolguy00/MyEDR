from datetime import datetime, timezone

from app.db.postgres import PostgresStore
from app.security.auth import create_access_token, decode_access_token, verify_password

class AuthService:
    def __init__(self, db:PostgresStore):
        self.db=db

    def login(self, username:str, password:str)->dict:
        user=self.db.fetch_one("SELECT id, username, password_hash, is_admin FROM users WHERE username = %s", (username,),)

        if not user:
            raise ValueError("Invalid username or password")

        if not verify_password(password, user["password_hash"]):
            raise ValueError("Invalid username or password")

        if not user["is_admin"]:
            raise PermissionError("Admin access required")


        token=create_access_token(user_id=user["id"], username=user["username"])

        return {"access_token": token, "token_type": "bearer"}


    def logout(self, token:str)->None:
        payload=decode_access_token(token)

        jti=payload["jti"]

        expires_at=datetime.fromtimestamp(payload["exp"], tz=timezone.utc)

        self.db.execute("INSERT INTO jwt_blocklist (jti, expires_at) VALUES (%s, %s) ON CONFLICT (jti) DO NOTHING", (jti, expires_at))


    def get_current_user(self, token:str)->dict:
        payload=decode_access_token(token)

        blocked = self.db.fetch_one("SELECT 1 FROM jwt_blocklist WHERE jti= %s", (payload["jti"],),)

        if blocked:
            raise ValueError("Token has been revoked")

        user=self.db.fetch_one("SELECT id, username, is_admin FROM users WHERE id = %s", (int(payload["sub"]),),)

        if not user:
            return ValueError("User not found")

        return user

        