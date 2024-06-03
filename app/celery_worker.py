from celery import Celery
from config import Config
from session import get_db
from app.models import Order
from flask import Flask


def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


app = Flask(__name__)
app.config.from_object(Config)
get_db.init_app(app)
celery = make_celery(app)


@celery.task
def update_order_status(order_id, status):
    order = Order.query.get(order_id)
    order.status = status
    get_db.session.commit()
    with open('order_status.log', 'a') as log:
        log.write(f"Order {order_id} changed status to {status}\n")
