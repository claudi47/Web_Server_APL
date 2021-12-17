from apscheduler.schedulers.background import BackgroundScheduler

# Declaration of a scheduler that will manage a queue of tasks, useful for managing transactions
transaction_scheduler = BackgroundScheduler()

def init_scheduler():
    transaction_scheduler.start()
