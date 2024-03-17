from email.message import Message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any

from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel

from src.infrastructure.config import settings
from src.domain.schemes import SUser

env = Environment(loader=FileSystemLoader("src/infrastructure/mail/templates"))
"""Шаблоны писем."""


def base_message(subject: str, user: SUser) -> Message:
    """Создание базового сообщения."""
    msg = MIMEMultipart("alternative")
    msg["From"] = settings.smtp.username
    msg["To"] = user.email
    msg["Subject"] = subject

    return msg


def render(template: str, subject: str, user: SUser, **kwargs) -> Message:
    """Рендер шаблона."""
    msg = base_message(subject, user)
    html = env.get_template(template).render(user=user, **kwargs)

    msg.attach(MIMEText(html, "html"))

    return msg


class MBase(BaseModel):
    template: str
    """Шаблон письма."""
    subject: str
    """Тема письма."""
    user: SUser
    """Адресат письма."""

    def render(self, **kwargs: Any) -> Message:
        """Рендер письма."""
        return render(self.template, self.subject, self.user, **kwargs)
