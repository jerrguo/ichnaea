import stepper_driver
import time

stepper_driver.move_stepper(1, 3000, 2)

time.sleep(2)

stepper_driver.move_stepper(0, 3000, 2)


#_DIR_PIN = 23
#_ENA_PIN = 24

#_SPEED_PINS = [11, 12, 13, 15]


#GPIO.setmode(GPIO.BOARD)
#GPIO.setup([_DIR_PIN, _ENA_PIN], GPIO.OUT, initial=GPIO.LOW)
#GPIO.setup(_SPEED_PINS, GPIO.OUT, initial=GPIO.LOW)

## finished and clean up
#GPIO.output(_ENA_PIN, GPIO.LOW)

#GPIO.cleanup()
