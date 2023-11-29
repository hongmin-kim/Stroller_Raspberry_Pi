import RPi.GPIO as GPIO
import time

# Pin Definition (GPIO.BOARD)
vibMotorA = 7
vibMotorB = 11

# Pin Definition (GPIO.BCM)
# vibMotorA = 4
# vibMotorB = 17

# Pin Setting
GPIO.setmode(GPIO.BOARD)
GPIO.setup(vibMotorA, GPIO.OUT)
GPIO.setup(vibMotorB, GPIO.OUT)

# Create a PWM object with frequency of 1000Hz
vibPwm1 = GPIO.PWM(vibMotorA, 1000)
vibPwm2 = GPIO.PWM(vibMotorB, 1000)

# Initialize with 0% duty cycle
vibPwm1.start(0)
vibPwm2.start(0)

print("70")
vibPwm1.ChangeDutyCycle(70)
vibPwm2.ChangeDutyCycle(0)
time.sleep(0.5)

vibPwm1.ChangeDutyCycle(0)
vibPwm2.ChangeDutyCycle(0)
time.sleep(1)


GPIO.cleanup()