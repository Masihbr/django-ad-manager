from celery import shared_task


@shared_task
def sum(a, b):
    return a + b
