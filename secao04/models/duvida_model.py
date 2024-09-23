from core.configs import settings
from models.area_model import AreaModel
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class DuvidaModel(settings.DBBaseModel):
    __tablename__ = "duvidas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_area: Mapped[int] = mapped_column(Integer, ForeignKey("areas.id"))
    area: Mapped[AreaModel] = relationship("AreaModel", back_populates="duvidas", lazy="joined")
    titulo: Mapped[str] = mapped_column(String(200))
    resposta: Mapped[str] = mapped_column(String(400))