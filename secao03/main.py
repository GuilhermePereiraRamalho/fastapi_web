from fastapi import FastAPI, UploadFile
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from aiofile import async_open
from uuid import uuid4


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")
media = Path('media')


@app.get("/")
async def index(request: Request, usuario: str = "Fortunato"):
    context = {
        "request": request,
        "usuario": usuario
    }

    return templates.TemplateResponse("index.html", context=context)

@app.get("/servicos")
async def servicos(request: Request):
    context = {
        "request": request,
    }

    return templates.TemplateResponse("servicos.html", context=context)


@app.post("/servicos")
async def cad_servicos(request: Request):
    form = await request.form()

    servico: str = form.get("servico")
    # print(f"Serviço: {servico}")

    arquivo: UploadFile = form.get("arquivo")
    # print(f"Nome do Arquivo: {arquivo.filename}")
    # print(f"Tipo do Arquivo: {arquivo.content_type}")

    arquivo_ext: str = arquivo.filename.split(".")[1]
    novo_nome: str = f"{str(uuid4())}.{arquivo_ext}"

    context = {
        "request": request,
        "imagem": novo_nome
    }

    async with async_open(f"{media}/{novo_nome}", "wb") as afile:
        await afile.write(arquivo.file.read())

    return templates.TemplateResponse("servicos.html", context=context)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)