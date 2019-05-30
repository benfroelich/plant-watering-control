# Plant watering system
## Introduction
This system monitors soil moisture and controls watering valves or pumps to 
water the plants. The watering algorithm will water at a specified interval,
but only if the soil moisture is sufficiently low. 

The system interface is not contained in this module; it is 
implemented in the web-based server at `../server`.

## SEN0193 and ADS1015 moisture sensing driver
### Calibration
calibration is stored in `./calibration.ini`. To calibrate, 
    python3 moisture_sensing.py
### Operation
`controller.py` will use `moisture_sensing.py`

## Datalogging module for the plant-watering project
### Usage

    log_data(23.5, "greenhouse-temperature", "degC")
    log_data(40, "cactus-watered", "mL")

see `generate-sample-datalog.py`
### Notes
logData stores data for a sensor or logpoint
sensorName can be any string. Keep it consistent for each measurement source.
