
import uvicorn
from fastapi import FastAPI
from route import routes
from fastapi.staticfiles import StaticFiles

import os
import uvicorn
app =FastAPI()
app.include_router(routes)

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run(app,host='0.0.0.0',port=8000)
