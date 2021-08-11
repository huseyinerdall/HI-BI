from apscheduler.schedulers.background import BackgroundScheduler
import json
from tasks import Tasks, mailing
import time

scheduler = BackgroundScheduler()

Tasks_ins = Tasks()

class Scheduler():
    def runTask(self, crontab, type, report, report_id):#the parameter crontab is crontab dictionary
        report_id = str(report_id)
        crontab = json.loads(crontab)
        print(crontab,type,report,report_id)

        def x(report_id):
            mailing(report_id=report_id)

        def y(b):
            time.sleep(10)
            print('Emailing'+b)

        if(type == 'Download locally'):
            
            func = y
            #func = Tasks_ins.exportPdf
            #arg = report
        elif(type == 'Emailing'):
            func = x
            #func = Tasks.mailing
            #arg = report

        minute = crontab[0]
        hour = crontab[1]
        dayOfMonth = crontab[2]#crontab['dayOfMonth']
        month = crontab[3]
        dayOfWeek = crontab[4]

        jobTemp = scheduler.add_job(func, 'cron',[report_id], minute=minute,hour=hour,day='*',month=month,day_of_week=dayOfWeek)
    scheduler.start()
    def taskList(self):
        return scheduler.get_jobs()
    def running(self):
        return scheduler.running
    def shutdownTasks(self):
        scheduler.shutdown(wait=False)

    def startTasks(self):
        scheduler.start()