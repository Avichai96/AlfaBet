# app/main.py

import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from routers import event, reminder


app = FastAPI()


# scheduler = BackgroundScheduler()
# scheduler.start()
# scheduler.add_job(EventReminder.send_reminders, 'interval', minutes=0.5)

# @app.on_event("shutdown")
# def shutdown_scheduler():
#     scheduler.shutdown()

app.include_router(event.router)
app.include_router(reminder.router)

def main():
    host="127.0.0.1"
    port=8080
    uvicorn.run("main:app", host=host, port=port, reload=True)


if __name__ == '__main__':
    main()