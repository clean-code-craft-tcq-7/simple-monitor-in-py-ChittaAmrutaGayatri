# monitor.py
import sys
import time
import random
from deep_translator import GoogleTranslator

LANGUAGE = "german"
STATES = ["HYPO", "NEAR_HYPO", "NORMAL", "NEAR_HYPER", "HYPER"]

VITALS = [
    {"name": "temperature", "minvalue": 95, "maxvalue": 102, "tol": 0.015, "unit": "F", "message": "Temperature critical!"},
    {"name": "pulserate", "minvalue": 60, "maxvalue": 100, "tol": 0.015, "unit": "bpm", "message": "Pulse Rate is out of range!"},
    {"name": "spo2", "minvalue": 90, "maxvalue": 100, "tol": 0.015, "unit": "%", "message": "Oxygen Saturation out of range!"},
    {"name": "blood-sugar", "minvalue": 70, "maxvalue": 110, "tol": 0.015, "unit": "mg/dl", "message": "Blood sugar levels out of range!"},
    {"name": "blood-pressure", "minvalue": 90, "maxvalue": 150, "tol": 0.015, "unit": "mmHg", "message": "Blood pressure levels out of range!"},
    {"name": "respiratory-rate", "minvalue": 12, "maxvalue": 20, "tol": 0.015, "unit": "bpm", "message": "Respiratory Rate out of range!"},
]

# ------------------------
# I/O Functions
# ------------------------
def display(message):
    """Display a translated message with animation"""
    print(translate(message, LANGUAGE))
    for _ in range(6):
        print("\r* ", end="")
        sys.stdout.flush()
        time.sleep(1)
        print("\r *", end="")
        sys.stdout.flush()
        time.sleep(1)
    return False

def translate(text, target):
    """Translate text to target language and uppercase it"""
    return GoogleTranslator(target=target).translate(text).upper()

# ------------------------
# Sensor simulation
# ------------------------
def sensorStub():
    """Simulate sensor readings"""
    return {vital["name"]: random.randint(vital["minvalue"], vital["maxvalue"]) for vital in VITALS}

# ------------------------
# Pure logic functions
# ------------------------
def is_vital_ok(value, min_value, max_value):
    """Check if a single vital is within range"""
    return min_value <= value <= max_value

def get_vital_state(vital_obj, value):
    """Return the state (HYPO, NORMAL, HYPER...) of a vital"""
    minvalue, maxvalue, tol = vital_obj["minvalue"], vital_obj["maxvalue"], vital_obj["tol"]
    tolvalue = maxvalue * tol
    thresholds = [
        (lambda v: v <= minvalue, "HYPO"),
        (lambda v: minvalue < v <= minvalue + tolvalue, "NEAR_HYPO"),
        (lambda v: minvalue + tolvalue < v <= maxvalue - tolvalue, "NORMAL"),
        (lambda v: maxvalue - tolvalue < v < maxvalue, "NEAR_HYPER"),
        (lambda v: v >= maxvalue, "HYPER"),
    ]
    for check, state in thresholds:
        if check(value):
            return state
    return "UNKNOWN"

# ------------------------
# High-level operations
# ------------------------
def report_vitals(sensor_data):
    """Print the state of each vital and check for critical values"""
    for vital in VITALS:
        value = sensor_data[vital["name"]]
        state = get_vital_state(vital, value)
        print(f"{vital['name']} - {state}")
        check_vitals(value, vital["minvalue"], vital["maxvalue"], vital["message"])

def check_vitals(value, min_value, max_value, message):
    """Check if vital is within range, display message if not"""
    return is_vital_ok(value, min_value, max_value) or display(message)

def vitals_ok(sensor_data):
    """Return True if all vitals are within range"""
    for vital in VITALS:
        if not check_vitals(sensor_data[vital["name"]], vital["minvalue"], vital["maxvalue"], vital["message"]):
            return False
    return True
