from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ExternalUser(Base):
    __tablename__ = "external_users"
    id: Mapped[int] = mapped_column(primary_key=True)  # our local id
    ext_id: Mapped[int] = mapped_column(index=True, unique=True)  # id from source
    email: Mapped[str | None] = mapped_column(String(255), index=True)
    name: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[str] = mapped_column(server_default=func.now())
