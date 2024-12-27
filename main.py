"""
Приложение FastAPI для сокращения ссылок
"""
import string
import random
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
from database import SessionLocal, Base, engine
from models import URLItem

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="URL Shortener API",
    description="API для сокращения ссылок с помощью FastAPI и SQLite. Позволяет создавать короткие ссылки, перенаправлять и получать статистику.",
    version="1.0.0"
)


class URLCreate(BaseModel):
    url: HttpUrl
    """
    Модель для создания короткой ссылки.
    - **url**: Полный URL, который требуется сократить.
    """


def get_db():
    """
    Зависимость для получения сессии базы данных.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def generate_short_id(length=6):
    """
    Генерация случайного короткого идентификатора из букв и цифр.
    - **length**: Длина идентификатора (по умолчанию 6 символов).
    """
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


@app.post("/shorten", response_description="Создать короткую ссылку")
def shorten_url(item: URLCreate, db: Session = Depends(get_db)):
    """
    Создает короткую ссылку из длинного URL.

    - **item**: JSON с полем `url` для сокращения.

    **Возвращает:**
    - **short_url**: Сокращенный URL, доступный по `http://localhost:8000/{short_id}`.

    **Ошибки:**
    - 500: Если не удалось сгенерировать уникальный идентификатор.
    """
    for _ in range(10):
        short_id = generate_short_id()
        existing = db.query(URLItem).filter(URLItem.short_id == short_id).first()
        if not existing:
            new_item = URLItem(short_id=short_id, full_url=str(item.url))
            db.add(new_item)
            db.commit()
            db.refresh(new_item)
            return {"short_url": f"http://localhost:8000/{short_id}"}
    raise HTTPException(status_code=500, detail="Не удалось сгенерировать короткую ссылку")


@app.get("/{short_id}", response_description="Перенаправить по короткой ссылке")
def redirect_to_full(short_id: str, db: Session = Depends(get_db)):
    """
    Перенаправляет на полный URL по короткой ссылке.

    - **short_id**: Идентификатор короткой ссылки.

    **Ошибки:**
    - 404: Если ссылка не найдена.
    """
    url_item = db.query(URLItem).filter(URLItem.short_id == short_id).first()
    if not url_item:
        raise HTTPException(status_code=404, detail="Короткая ссылка не найдена")
    return RedirectResponse(url=url_item.full_url)


@app.get("/stats/{short_id}", response_description="Получить статистику по короткой ссылке")
def get_stats(short_id: str, db: Session = Depends(get_db)):
    """
    Возвращает статистику по сокращенной ссылке без перенаправления.

    - **short_id**: Идентификатор короткой ссылки.

    **Возвращает:**
    - **short_id**: Уникальный идентификатор ссылки.
    - **full_url**: Исходная длинная ссылка.

    **Ошибки:**
    - 404: Если ссылка не найдена.
    """
    url_item = db.query(URLItem).filter(URLItem.short_id == short_id).first()
    if not url_item:
        raise HTTPException(status_code=404, detail="Короткая ссылка не найдена")
    return {
        "short_id": url_item.short_id,
        "full_url": url_item.full_url
    }
