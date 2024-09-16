from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request


app = FastAPI(docs_url=None, redoc_url=None)
templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory='static'), name='static')
app.mount('/media', StaticFiles(directory='media'), name='media')

@app.get("/", name="index")
async def index(request: Request):
    context = {
        "request": request
    }
    return templates.TemplateResponse("home/index.html", context=context)


@app.get("/about", name="about")
async def about(request: Request):
    context = {
        "request": request
    }
    return templates.TemplateResponse("home/about.html", context=context)


@app.get("/contact", name="contact")
async def contact(request: Request):
    context = {
        "request": request
    }
    return templates.TemplateResponse("home/contact.html", context=context)


@app.get("/pricing", name="pricing")
async def pricing(request: Request):
    context = {
        "request": request
    }
    return templates.TemplateResponse("home/pricing.html", context=context)


@app.get("/faq", name="faq")
async def faq(request: Request):
    context = {
        "request": request
    }
    return templates.TemplateResponse("home/faq.html", context=context)


@app.get("/blog-home", name="blog-home")
async def blog_home(request: Request):
    context = {
        "request": request
    }
    return templates.TemplateResponse("home/blog_home.html", context=context)


@app.get("/blog-post", name="blog-post")
async def blog_post(request: Request):
    context = {
        "request": request
    }
    return templates.TemplateResponse("home/blog_post.html", context=context)


@app.get("/portfolio-overview", name="portfolio-overview")
async def portfolio_overview(request: Request):
    context = {
        "request": request
    }
    return templates.TemplateResponse("home/portfolio_overview.html", context=context)


@app.get("/portfolio-item", name="portfolio-item")
async def portfolio_item(request: Request):
    context = {
        "request": request
    }
    return templates.TemplateResponse("home/portfolio_item.html", context=context)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app='main:app', host='0.0.0.0', port=8000, log_level='info', reload=True)