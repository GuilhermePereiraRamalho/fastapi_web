from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI(docs_url=None, redoc_url=None)
templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory='static'), name='static')
app.mount('/media', StaticFiles(directory='media'), name='media')


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app='main:app', host='0.0.0.0', port=8000, log_level='info', reload=True)