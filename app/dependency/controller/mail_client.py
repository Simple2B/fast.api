from functools import lru_cache
from fastapi import Depends
from app.controller import MailClient
from app.config import Settings, get_settings


@lru_cache
def get_mail_client(settings: Settings = Depends(get_settings)) -> MailClient:
    return MailClient(settings)
