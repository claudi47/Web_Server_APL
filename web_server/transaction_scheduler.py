import datetime
import functools

from apscheduler.schedulers.background import BackgroundScheduler

from web_server.job_stores import job_stores

# Declaration of a scheduler that will manage a queue of tasks, useful for managing transactions
transaction_scheduler = BackgroundScheduler(jobstores=job_stores)


def init_scheduler():
    transaction_scheduler.start()


def repeat_deco(repeat_count, reschedule_count=0, always_reschedule=False):
    def deco_wrapper(func):
        @functools.wraps(func)
        def func_wrapper(trans_id, *args, **kwargs):
            counter = 0
            while counter < repeat_count:
                try:
                    return func(trans_id, *args, **kwargs)
                except:
                    counter += 1
            if func_wrapper.reschedule_count > 0:
                if not always_reschedule:
                    func_wrapper.reschedule_count -= 1
                transaction_scheduler.add_job(func_wrapper,
                                              id=str(trans_id),
                                              run_date=datetime.datetime.now() + datetime.timedelta(seconds=5),
                                              args=[trans_id, *args], kwargs=kwargs, replace_existing=True, misfire_grace_time=3600)

            raise Exception(f'Failed execution in function: {func.__name__!r}')

        func_wrapper.reschedule_count = reschedule_count
        return func_wrapper

    return deco_wrapper


