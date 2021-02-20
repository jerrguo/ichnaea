import time
import RPi.GPIO as GPIO

_DIR_PIN = 18
_ENA_PIN = 19
_SPEED_PINS = [21, 22, 23, 24]
###
### direction = 1 = forward
###
def move_stepper(direction, duration, speed):
    if direction != 1 and direction != 0:
        raise ValueError("Invalid direction")
    if not 0 <= speed <= 4:
        raise ValueError("Invalid Speed")

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup([_DIR_PIN, _ENA_PIN], GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(_SPEED_PINS, GPIO.OUT, initial=GPIO.LOW)
    
    ## set up speed data lines:
    for i in range(speed):
        GPIO.output(_SPEED_PINS[i], GPIO.HIGH)
    
    ## set direction
    GPIO.output(_DIR_PIN, direction)

    ## data valid, start the motor
    GPIO.output(_ENA_PIN, GPIO.HIGH)

    ## wait for required duration
    time.sleep(duration)

    ## finished and clean up
    GPIO.output(_ENA_PIN, GPIO.LOW)
    
    GPIO.cleanup()
