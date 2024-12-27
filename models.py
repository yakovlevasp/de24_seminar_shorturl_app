"""
Модель для хранения сокращенных URL
"""
from sqlalchemy import Column, Integer, String
from database import Base


class URLItem(Base):
    """
    Модель SQLAlchemy для хранения сокращенных URL.

    Атрибуты:
    - **id** (int): Уникальный идентификатор записи, первичный ключ.
    - **short_id** (str): Уникальный короткий идентификатор для сокращенной ссылки.
    - **full_url** (str): Полный URL, который был сокращен.
    """
    __tablename__ = "short_urls"

    id = Column(Integer, primary_key=True, index=True)
    short_id = Column(String, unique=True, index=True)
    full_url = Column(String)
