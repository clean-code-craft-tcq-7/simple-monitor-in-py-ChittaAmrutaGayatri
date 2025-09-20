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

def display(message):
    """Display a translated message with simple animation"""
    translated_message = translate(message, LANGUAGE)
    print(translated_message)
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

def sensorStub():
    """Simulate sensor readings"""
    return {vital["name"]: random.randint(vital["minvalue"], vital["maxvalue"]) for vital in VITALS}

def is_inrange(value, min_value, max_value):
    """Check if value is in range"""
    return min_value <= value <= max_value

def check_vitals(value, min_value, max_value, message):
    """Check if vital is within range, otherwise display message"""
    return is_inrange(value, min_value, max_value) or display(message)

def calculate_ranges(obj):
    """Generate threshold ranges for a vital"""
    minvalue, maxvalue, tol = obj["minvalue"], obj["maxvalue"], obj["tol"]
    tolvalue = maxvalue * tol
    return [
        lambda val: val <= minvalue,
        lambda val: minvalue < val <= minvalue + tolvalue,
        lambda val: minvalue + tolvalue < val <= maxvalue - tolvalue,
        lambda val: maxvalue - tolvalue < val < maxvalue,
        lambda val: val >= maxvalue,
    ]

def print_status(obj, value):
    """Print the status of a vital based on predefined states"""
    ranges = calculate_ranges(obj)
    for index, check in enumerate(ranges):
        if check(value):
            print(f"{obj['name']} - {STATES[index]}")
            break
    return True

def vitals_ok(sensor_data):
    """Check all vitals and return overall status"""
    for obj in VITALS:
        value = sensor_data[obj["name"]]
        print_status(obj, value)
        if not check_vitals(value, obj["minvalue"], obj["maxvalue"], obj["message"]):
            return False
    return True
