from starlette.staticfiles import StaticFiles
from fastapi import FastAPI

from .routers import api, ws

app = FastAPI()

app.include_router(api.router)
app.include_router(ws.router)

app.mount("/", StaticFiles(directory="web/", html=True), name="web")

if __name__ == '__main__':
    import uvicorn

    #TODO get arguments from env/cli
    uvicorn.run('app:app', host='127.0.0.1', port=9000, reload=False, log_level='debug')
