from core.configs import settings
from typing import List
from sqlalchemy.orm import relationship, Mapped, mapped_column

class AreaModel(settings.DBBaseModel):
    __tablename__: str = "areas"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()


    duvidas: Mapped[List["DuvidaModel"]] = relationship("DuvidaModel", back_populates="area", lazy="joined")