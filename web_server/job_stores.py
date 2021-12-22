from apscheduler.jobstores.mongodb import MongoDBJobStore
import os

job_stores = {
    'default': MongoDBJobStore(host=f'mongodb+srv://claudi47:{os.getenv("mongodb_Password")}@apldb.hhz9g.mongodb.net/db_apl?retryWrites=true&w=majority')
}