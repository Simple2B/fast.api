import pytest
from app.controller import MailClient
from app.config import Settings
from tests.conftest import get_test_settings


@pytest.fixture
def mail_client() -> MailClient:
    settings: Settings = get_test_settings()
    return MailClient(settings)
