from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from parser import get_page_text
from ner_model import extract_products, get_most_popular

app = FastAPI(title="Furniture Product Extractor")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/extract", response_class=HTMLResponse)
async def extract(request: Request, url: str = Form(...)):
    try:
        text = get_page_text(url)
        if not text:
            return templates.TemplateResponse("index.html", {
                "request": request,
                "products": [],
                "error": "Не удалось получить текст со страницы"
            })
        products = extract_products(text)
        most_popular = get_most_popular(products)
        return templates.TemplateResponse("index.html", {
            "request": request,
            "products": products,
            "most_popular": most_popular
        })
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "products": [],
            "error": f"Произошла ошибка: {str(e)}"
        })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)
