import asyncio
import manual_controls
import controller_status
import sequencer
import settings as settings_file

async def main():
    await sequencer.generate_schedule()
    pause_schedule = sequencer.run_continuously()

    await asyncio.gather(
        manual_controls.serve(pause_schedule),
        monitor_settings(pause_schedule)
    )

async def monitor_settings(pause_schedule, interval=1):
    while True:
        await asyncio.sleep(interval)
        if await settings_file.new_settings(): 
            pause_schedule.set()
            await sequencer.generate_schedule()
            pause_schedule.clear()

if __name__ == "__main__":
    asyncio.run(main())

# WIP
def test():
    print("checking watering utilities")
    do_watering(**{
        "watering_settings":    {
             "name": "Lechuga",
             "in_ch": 2,
             "out_ch": 1,
             "interval_days": 1,
             "duration_mins": 1,
             "time_of_day": ["00:00", "11:00"],
             "thresh_en": "on",
             "thresh_pct": 50,
             "zone_en": "on"
        }
    })
    # TODO
    # unit test of schedule generator/reader of json file
    # unit test of HW control
    # integration test here
