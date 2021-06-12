import RPi.GPIO as GPIO
import time

pin_no = 24

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin_no, GPIO.OUT)
try:
    while True:
        GPIO.output(pin_no, True)
        time.sleep(0.5)
        GPIO.output(pin_no, False)
        time.sleep(0.5)
except KeyboardInterrupt:
    pass

GPIO.cleanup()
