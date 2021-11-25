#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
import threading
import datetime
import logging

BUTTON = 2                   # GPIO pin for Hardware button
BELL_RELAY = 27              # GPIO pin for Relay           
RING_TRIGGER_LENGTH = .050   # Time needed to ring bell cleanly (not overdrive solenoid)
RING_COOLDOWN_LENGTH = 4     # Time delay between when rings will be permitted
TIME_GUARD = "ON"            # Guard to prevent bell from ringing too early or late,(New Years Eve?)
TIME_GUARD_START = 10        # Earliest hour the bell can ring when Time Guard is on 
TIME_GUARD_END = 21          # Latest hour the bell can ring when Time Guard is on (24 hr format)

last_ring_time = time.time()

def initialize():
     GPIO.setwarnings(False)         # Disable warning mesages for GPIO
     GPIO.setmode(GPIO.BCM)          # Set to use Boardcom pin numbering

     # Configure GPIO port 27 as Output to use as relay trigger, initial value set to not triggered
     # Hardware: Connect jumper from GPIO port 27 to Relay board signal pin
     GPIO.setup(BELL_RELAY, GPIO.OUT, initial=GPIO.HIGH)     

     # Configure GPIO port 2 as Input for Hardware button, Use built in pull Up resistor
     # Hardware: Connect Button leads to GPIO port2 and GPIO ground pin
     GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

     # Detect Button pushes and then do callback to ring function
     GPIO.add_event_detect(BUTTON, GPIO.RISING, callback=button_callback, bouncetime=200)

def button_callback(channel):
    logging.info('Button on Bell-Ringer box pressed at           ')
    ringOnce()

def ringOnce():
     currentHour = int(time.strftime("%H"))   # get current hour as an integer

     if TIME_GUARD == "ON" and currentHour not in range(TIME_GUARD_START, TIME_GUARD_END):  
          logging.info('   Ring requested but outside of allowed hours ')
          return 403

     global last_ring_time

     now = time.time()
     time_since_last_ring = int(now - last_ring_time)

     if time_since_last_ring < RING_COOLDOWN_LENGTH:
          logging.info('   Ring requested but still in CoolDown period ')
          return 429

     last_ring_time = now

     GPIO.output(BELL_RELAY, GPIO.LOW)   # Set GPIO output to trigger the relay
     time.sleep(RING_TRIGGER_LENGTH)     # Keep GPIO output triggered necessary time to pull clapper
     GPIO.output(BELL_RELAY, GPIO.HIGH)  # Set GPIO output to reset/relax the relay
     logging.info('   BELL WENT BONG to honor request             ')
     return 200

def cleanup():
     GPIO.cleanup()                      # GPIO cleanup for a clean exit (reset ports used)

