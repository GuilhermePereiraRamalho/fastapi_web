from typing import List
import sqlalchemy.orm as orm
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.configs import settings
from models.tag_model import TagModel

tags_autor = Table(
    "tags_autor",
    settings.DBBaseModel.metadata,
    Column("id_autor", Integer, ForeignKey("autores.id")),
    Column("id_tag", Integer, ForeignKey("tags.id"))
)


class AutorModel(settings.DBBaseModel):
    __tablename__: str = "autores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100))
    imagem: Mapped[str] = mapped_column(String(100))  # 40x40

    tags: Mapped[List[TagModel]] = relationship(
        'TagModel', 
        secondary=tags_autor, 
        backref="taga", 
        lazy="joined"
    )

    @property
    def get_tags_list(self):
        lista: List[int] = []

        for tag in self.tags:
            lista.append(int(tag.id))
        
        return lista