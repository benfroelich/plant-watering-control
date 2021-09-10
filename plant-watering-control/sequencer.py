import settings as settings_file
import threading
import schedule
import time
import irrigation_tasks

def run_continuously(interval=1):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return pause: threading Event which can
    be set to pause continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    pause = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while True:
                if not pause.is_set():
                    schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return pause

async def generate_schedule():
    print("generating schedule")
    schedule.clear() # remove all jobs
    
    # build complete schedule from file 
    settings = await settings_file.load_settings()
    
    for i,cfg in enumerate(settings["zones"]):
        if "zone_en" in cfg:
            for time in cfg["time_of_day"]:
                schedule.every(cfg["interval_days"]).days.at(time).do(
                    irrigation_tasks.do_watering, 
                    **{
                        "watering_settings": cfg,
                    }
                )
    schedule.every(settings["moisture_interval_minutes"]).minutes.do(irrigation_tasks.log_moisture)
    schedule.every(settings["reservoir"]["interval_minutes"]).minutes.do(irrigation_tasks.check_reservoir, 
            **{"settings": settings})
