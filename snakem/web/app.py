from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .routers import api, view, ws

app = FastAPI()

app.include_router(api.router)
app.include_router(ws.router)

app.include_router(view.router)

@app.get("/", response_class=RedirectResponse)
async def view_root():
    return '/view'

if __name__ == '__main__':
    import uvicorn

    #TODO get arguments from env/cli
    uvicorn.run('app:app', host='127.0.0.1', port=9000, reload=False, log_level='debug')
