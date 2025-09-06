
from time import sleep
import sys


# monitor.py

VITAL_LIMITS = {
    "temperature": (95, 102),   # min, max
    "pulseRate": (60, 100),
    "spo2": (90, None)          # None = no upper limit
}


def is_vital_ok(name, value):
    min_val, max_val = VITAL_LIMITS[name]
    if (min_val is not None and value < min_val) or (max_val is not None and value > max_val):
        return False
    return True


def vitals_status(temperature, pulseRate, spo2):
    return {
        "temperature": is_vital_ok("temperature", temperature),
        "pulseRate": is_vital_ok("pulseRate", pulseRate),
        "spo2": is_vital_ok("spo2", spo2),
    }


def vitals_ok(temperature, pulseRate, spo2):
    return all(vitals_status(temperature, pulseRate, spo2).values())


def report_vitals(temperature, pulseRate, spo2):
    status = vitals_status(temperature, pulseRate, spo2)

    if not status["temperature"]:
        print("Temperature is out of range.")
    if not status["pulseRate"]:
        print("Pulse rate is out of range.")
    if not status["spo2"]:
        print("Oxygen saturation is out of range.")

    return all(status.values())
