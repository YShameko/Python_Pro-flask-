from celery import Celery
import os

from sqlalchemy import select

from database import db_session, init_db
from models import Contract
service_email = 'service@example.com'
service_email_pass = '1234'
# -------------------------------------------------------------------------------------------
# app = Celery('tasks', broker='redis://localhost:6379/0')
app = Celery('tasks', broker=f'pyamqp://guest@{os.environ.get("RABBITMQ_HOST", "localhost")}//')

@app.task
def add(x, y):
    print(x + y)

@app.task
def send_email(contract_id):
    import smtplib

    init_db()
    # should get takers email, leasers email, contracts text, but a bit later
    # contract = db_session.execute(select(Contract).filter_by(id == contract_id)).scalar()
    # item = list(db_session.execute(select(models.Item).where(models.Item.id == item_id)).scalar())
    message = 'Text to be sent'
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(service_email, service_email_pass)
    s.sendmail(service_email, 'user1@example.com', message)
    s.sendmail(service_email, 'user2@example.com', message)
    s.quit()
