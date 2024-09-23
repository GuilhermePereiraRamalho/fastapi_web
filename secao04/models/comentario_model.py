from datetime import datetime
import sqlalchemy.orm as orm
from core.configs import settings
from models.post_model import PostModel
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class ComentarioModel(settings.DBBaseModel):
    __tablename__: str = "comentarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    data: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True)
    id_post: Mapped[int] = mapped_column(Integer, ForeignKey("posts.id"))
    
    post: Mapped[PostModel] = relationship("PostModel", back_populates="comentarios")
    
    autor: Mapped[str] = mapped_column(String(200))
    texto: Mapped[str] = mapped_column(String(400))
