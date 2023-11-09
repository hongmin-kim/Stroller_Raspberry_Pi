import RPi.GPIO as GPIO
import time

# Pin Definition
vibMotorA = 7
vibMotorB = 11

# Pin Setting
GPIO.setmode(GPIO.BOARD) # no breadboard
GPIO.setup(vibMotorA, GPIO.OUT)
GPIO.setup(vibMotorB, GPIO.OUT)

# Create a PWM object with frequency of 1000Hz
vibPwm1 = GPIO.PWM(vibMotorA, 1000)
vibPwm2 = GPIO.PWM(vibMotorB, 1000)

# Initialize with 0% duty cycle
vibPwm1.start(0)
vibPwm2.start(0)

vibPwm1.ChangeDutyCycle(50)
vibPwm2.ChangeDutyCycle(0)
time.sleep(3)
vibPwm1.ChangeDutyCycle(0)
vibPwm2.ChangeDutyCycle(50)
time.sleep(3)
vibPwm1.ChangeDutyCycle(0)
vibPwm2.ChangeDutyCycle(0)
time.sleep(1.5)

# rise_start_time = time.time()

# for duty in range(0, 101):
#     elapsed_time = time.time() - rise_start_time

#     target_time = duty / 100
            
#     while elapsed_time < target_time:
#         elapsed_time = time.time() - rise_start_time

#         vibPwm1.ChangeDutyCycle(duty)
#         vibPwm2.ChangeDutyCycle(0)

# burst_start_time = time.time()
        
# while (1):
#     current_time = time.time()

#     if (current_time - burst_start_time <= 0.2):
#         print("elapsed: {}".format(current_time - burst_start_time))
#         vibPwm1.ChangeDutyCycle(100) # short burst of high-intensity vibration
#         vibPwm2.ChangeDutyCycle(0)
#     elif (current_time - burst_start_time <= 0.4):
#         print("elapsed: {}".format(current_time - burst_start_time))
#         vibPwm1.ChangeDutyCycle(0)
#         vibPwm2.ChangeDutyCycle(0)
#     elif (current_time - burst_start_time <= 0.6):
#         print("elapsed: {}".format(current_time - burst_start_time))
#         vibPwm1.ChangeDutyCycle(100)
#         vibPwm2.ChangeDutyCycle(0)        
#     elif (current_time - burst_start_time <= 0.8):
#         print("elapsed: {}".format(current_time - burst_start_time))
#         vibPwm1.ChangeDutyCycle(100)
#         vibPwm2.ChangeDutyCycle(0)
#     else:
#         print("elapsed: {}".format(current_time - burst_start_time))
#         vibPwm1.ChangeDutyCycle(0)
#         vibPwm2.ChangeDutyCycle(0)
#         break

GPIO.cleanup()