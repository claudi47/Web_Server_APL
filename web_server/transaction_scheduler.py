import datetime

from apscheduler.schedulers.background import BackgroundScheduler

# Declaration of a scheduler that will manage a queue of tasks, useful for managing transactions
transaction_scheduler = BackgroundScheduler()


def init_scheduler():
    transaction_scheduler.start()


def repeat_n_times_until_success(transaction, count, *args, reschedule_count=0,
                                 always_reschedule=False):
    """
    Schedule a function to ensure execution

    @param transaction: the function to be executed
    @param count: number of times to for retry
    @param args: arguments to pass to the function
    @param reschedule_count: number of times to reschedule (ignored if always_reschedule is True)
    @param always_reschedule: if True, the function will be executed every time until success
    @return: True if the function is successfully executed, False otherwise
    """
    counter = 0
    while counter < count:
        try:
            transaction(*args)
            return True
        except Exception as ex:
            counter += 1

    if reschedule_count > 0:
        transaction_scheduler.add_job(repeat_n_times_until_success, 'date',
                                      run_date=datetime.datetime.now() + datetime.timedelta(seconds=5),
                                      args=[transaction, count, *args],
                                      kwargs={
                                          'reschedule_count': reschedule_count - 1 if not always_reschedule else reschedule_count,
                                          'always_reschedule': always_reschedule})
    return False
