from typing import List

from fastapi.requests import Request
from fastapi import UploadFile

from aiofile import async_open

from uuid import uuid4

from core.configs import settings
from core.database import get_session
from models.post_model import PostModel
from controllers.base_controller import BaseController


class PostController(BaseController):

    def __init__(self, request: Request) -> None:
        super().__init__(request, PostModel)
    
    async def post_crud(self) -> None:
        form = await self.request.form()
        
        titulo: str = form.get('titulo')
        tags: List[str] = form.getlist('tag')
        imagem: UploadFile = form.get('imagem')
        texto: str = form.get('texto')
        autor_id: int = form.get('autor')

        arquivo_ext: str = imagem.filename.split('.')[-1]
        novo_nome: str = f"{str(uuid4())}.{arquivo_ext}"

        post: PostModel = PostModel(titulo=titulo, imagem=novo_nome, texto=texto, id_autor=int(autor_id))
        
        for id_tag in tags:
            tag = await self.get_tag(id_tag=int(id_tag))
            post.tags.append(tag)

        async with async_open(f"{settings.MEDIA}/post/{novo_nome}", "wb") as afile:
            await afile.write(imagem.file.read())
        
        async with get_session() as session:
            session.add(post)
            await session.commit()
 

    async def put_crud(self, obj: object) -> None:
        async with get_session() as session:
            post: PostModel = await session.get(self.model, obj.id)

            if post:
                form = await self.request.form()

                titulo: str = form.get('titulo')
                tags: List[str] = form.getlist('tag')
                imagem: UploadFile = form.get('imagem')
                texto: str = form.get('texto')
                autor_id: int = form.get('autor')

                if titulo and titulo != post.titulo:
                    post.titulo = titulo
                if tags:
                    post.tags = []
                    await session.commit()
                    for id_tag in tags:
                        tag = await self.get_tag(id_tag=int(id_tag))
                        tag_local = await session.merge(tag)
                        post.tags.append(tag_local)
                if texto and texto != post.texto:
                    post.texto = texto
                if autor_id and autor_id != post.autor.id:
                    post.id_autor = int(autor_id)
                if imagem.filename:
                    arquivo_ext: str = imagem.filename.split('.')[-1]
                    novo_nome: str = f"{str(uuid4())}.{arquivo_ext}"
                    post.imagem = novo_nome
                    async with async_open(f"{settings.MEDIA}/post/{novo_nome}", "wb") as afile:
                        await afile.write(imagem.file.read())
                await session.commit()

