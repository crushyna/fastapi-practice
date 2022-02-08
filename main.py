from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from auth import authentication
from db import models
from db.database import engine
from exceptions import StoryException
from router import blog_get, user, article, product, blog_post, file
from fastapi.staticfiles import StaticFiles
from templates import templates
import time

app = FastAPI()
app.include_router(templates.router)
app.include_router(authentication.router)
app.include_router(file.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(product.router)


@app.get('/hello',
         tags=['blog']
         )
def index():
    return {'message': 'Hello World'}


# @app.get('/blog/all')
# def get_all_blogs():
#     return {'message': 'All blogs provided'}


# default values
# @app.get('/blog/all')
# def get_all_blogs(page=1, page_size=10):
#     return {'message': f'All {page_size} blogs on page {page}'}

@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(
        status_code=418,
        content={'detail': exc.name}
    )


# @app.exception_handler(HTTPException)
# def custom_handler(request: Request, exc: StoryException):
#     return PlainTextResponse(str(exc), status_code=400)


models.Base.metadata.create_all(engine)


@app.middleware("http")
async def add_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers['duration'] = str(duration)

    return response


origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=['*']
)

app.mount('/files', StaticFiles(directory="files"), name='files')
app.mount('/templates/static', StaticFiles(directory="templates/static"), name='static')
