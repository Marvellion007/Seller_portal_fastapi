import sys
sys.path.append("..")
sys.path.append("../..")
from fastapi import FastAPI
from core.controller import message

app = FastAPI()

app.include_router(message.router)




