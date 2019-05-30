SEN0193 and ADS1015 moisture sensing driver


# Datalogging module for the plant-watering project
## Usage
'''
log_data(23.5, "greenhouse-temperature", "degC")
log_data(40, "cactus-watered", "mL")
'''
see generate-sample-datalog.py
## Notes
logData stores data for a sensor or logpoint
sensorName can be any string. Keep it consistent for each measurement source.
