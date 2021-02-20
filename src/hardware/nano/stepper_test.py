import stepper_driver
import time


stepper_driver.move_stepper(1, 3, 4)
print("Done movement 1")


time.sleep(1)

stepper_driver.move_stepper(0, 3, 4)
print("Done movement 2")

#_DIR_PIN = 23
#_ENA_PIN = 24

#_SPEED_PINS = [11, 12, 13, 15]


#GPIO.setmode(GPIO.BOARD)
#GPIO.setup([_DIR_PIN, _ENA_PIN], GPIO.OUT, initial=GPIO.LOW)
#GPIO.setup(_SPEED_PINS, GPIO.OUT, initial=GPIO.LOW)

## finished and clean up
#GPIO.output(_ENA_PIN, GPIO.LOW)

#GPIO.cleanup()
