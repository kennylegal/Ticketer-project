from ninja import Schema
from datetime import datetime

class EventIn(Schema):
    user: str
    title: str
    description: str = ""
    date: datetime
    venue: str
    image_url: str | None = None

class EventOut(Schema):
    id: int
    title: str
    description: str
    date: datetime
    image: str | None = None

