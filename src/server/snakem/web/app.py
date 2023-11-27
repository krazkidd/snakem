from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from .routers import api, ws

app = FastAPI()

#TODO should this only be enabled for local dev?
#     should i be explicit about allowed origin? (http://localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    #TODO requires allowed_origins != "*"
    #allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router)
app.include_router(ws.router)

if __name__ == '__main__':
    import uvicorn

    #TODO get arguments from env/cli
    uvicorn.run('app:app', host='127.0.0.1', port=9000, reload=False, log_level='debug')
