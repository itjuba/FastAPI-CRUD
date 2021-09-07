from fastapi import FastAPI, Request
from accounts import urls
app = FastAPI()

app.include_router(urls.router)








@app.get("/")
async def Hello(request: Request):

    return {"title" : "Welcome to FastAPI",
    "Host": request.client ,

            "Ali ramdani" : "Hello from fastAPI alilo"}
