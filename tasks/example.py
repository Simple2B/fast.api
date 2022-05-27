from invoke import task


@task
def time(_):
    """this is sample task - print current time"""
    from datetime import datetime

    now: datetime = datetime.now()
    print(now.strftime("%H:%M"))
