# app/main.py

import uvicorn
from fastapi import FastAPI
from routers import event, reminder
from middlewares import RateLimitMiddleware


app = FastAPI()

app.add_middleware(RateLimitMiddleware, limit_string="10")

app.include_router(event.router)
app.include_router(reminder.router)

def main():
    host="127.0.0.1"
    port=8080
    uvicorn.run("main:app", host=host, port=port, reload=True)


if __name__ == '__main__':
    main()