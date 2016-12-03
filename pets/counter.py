from apscheduler.schedulers.background import BackgroundScheduler


class PetStatCounter(object):

    scheduler = BackgroundScheduler()

    @staticmethod
    def start():
        PetStatCounter.scheduler.start()

    @staticmethod
    def status():
        PetStatCounter.scheduler.print_jobs()

    @staticmethod
    def add_job(function, interval, name):
        PetStatCounter.scheduler.add_job(function, 'interval', seconds=interval, id=name)

    @staticmethod
    def remove_job(name):
        PetStatCounter.scheduler.remove_job(name)
