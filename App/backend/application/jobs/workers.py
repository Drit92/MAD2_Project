from celery import Celery, Task
from application.jobs import celeryconfig

from flask import current_app as app

cel = Celery('application_jobs')

class ContextTask(cel.Task):
    def __call__(self, *args, **kwds):
        with app.app_context():
            return super().__call__(*args, **kwds)

def create_celery_app(app):
    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(celeryconfig)
    return celery_app




