from typing import List, Optional
from sqlalchemy.future import select
from fastapi.requests import Request
from fastapi import UploadFile
from aiofile import async_open
from uuid import uuid4
from core.configs import settings
from core.database import get_session
from models.autor_model import AutorModel
from controllers.base_controller import BaseController


class AutorController(BaseController):

    def __init__(self, request: Request) -> None:
        super().__init__(request, AutorModel)


    async def get_all_crud(self) -> Optional[List[AutorModel]]:
        async with get_session() as session:
            query = select(self.model)
            result = await session.execute(query)

            return result.scalars().unique().all()
    

    async def post_crud(self) -> None:
        form = await self.request.form()
        
        nome: str = form.get('nome')
        imagem: UploadFile = form.get('imagem')
        tags: List[str] = form.getlist('tag')

        arquivo_ext: str = imagem.filename.split('.')[-1]
        novo_nome: str = f"{str(uuid4())}.{arquivo_ext}"

        autor: AutorModel = AutorModel(nome=nome, imagem=novo_nome)

        for id_tag in tags:
            tag = await self.get_tag(id_tag=int(id_tag))
            autor.tags.append(tag)

        async with async_open(f"{settings.MEDIA}/autor/{novo_nome}", "wb") as afile:
            await afile.write(imagem.file.read())
        
        async with get_session() as session:
            session.add(autor)
            await session.commit()
 

    async def put_crud(self, obj: object) -> None:
        async with get_session() as session:
            autor: AutorModel = await session.get(self.model, obj.id)

            if autor:
                form = await self.request.form()

                nome: str = form.get('nome')
                imagem: UploadFile = form.get('imagem')
                tags: List[str] = form.getlist('tag')

                if nome and nome != autor.nome:
                    autor.nome = nome
                if tags:
                    autor.tags = []
                    await session.commit()
                    for id_tag in tags:
                        tag = await self.get_tag(id_tag=int(id_tag))
                        tag_local = await session.merge(tag)
                        autor.tags.append(tag_local)
                if imagem.filename:
                    arquivo_ext: str = imagem.filename.split('.')[-1]
                    novo_nome: str = f"{str(uuid4())}.{arquivo_ext}"
                    autor.imagem = novo_nome
                    async with async_open(f"{settings.MEDIA}/autor/{novo_nome}", "wb") as afile:
                        await afile.write(imagem.file.read())
                await session.commit()

