from typing import Optional

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.config import Settings, get_settings
from app.database import get_db
import app.model as m
import app.schema as s
from app.oauth2 import (
    INVALID_CREDENTIALS_EXCEPTION,
    create_access_token,
    verify_access_token,
)

settings: Settings = get_settings()
db = get_db().__next__()


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email = form["email"]
        password = form["password"]
        superuser = m.SuperUser.authenticate(db, email, password)
        if not superuser:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        session_token = create_access_token(data={"user_id": superuser.id})
        # And update session
        request.session.update({"token": session_token})

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        session_token = request.session.get("token")
        if not session_token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        token_data: s.TokenData = verify_access_token(
            session_token, INVALID_CREDENTIALS_EXCEPTION
        )
        if not db.query(m.SuperUser).filter_by(id=token_data.user_id).first():
            return False
        return True


authentication_backend = AdminAuth(secret_key=settings.JWT_SECRET)
