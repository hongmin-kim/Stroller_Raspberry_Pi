import RPi.GPIO as GPIO
import time

# # Pin Definition
# vibMotorA = 7
# vibMotorB = 11

# # Pin Setting
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(vibMotorA, GPIO.OUT)
# GPIO.setup(vibMotorB, GPIO.OUT)

# # Create a PWM object with frequency of 1000Hz
# vibPwm1 = GPIO.PWM(vibMotorA, 1000)
# vibPwm2 = GPIO.PWM(vibMotorB, 1000)

# # Initialize with 0% duty cycle
# vibPwm1.start(0)
# vibPwm2.start(0)

# # Variable for "Rise" vibraiton pattern
# step_time = 0.01

def alarm_vibration(response_queue):
    # Pin Definition
    vibMotorA = 7
    vibMotorB = 11

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

    # Variable for "Rise" vibraiton pattern
    step_time = 0.01
    # Parse sound classification arriving from server
    # Note that in send_audio.py, response_data is a dictionary
    # response_data ex: {'Alarm': False, 'Label': 'Infant Crying', 'Tagging_rate': 0.00, 'Switch': True}
    while True:
        response_data = response_queue.get() # retrieve data from the queue. Waits for data to arrive in real-time.
        #print("vib_motor_process - response_data['Label']: {}".format(response_data['Label']))

        if ( response_data['Alarm'] and response_data['Switch'] and response_data['Label'] == 'Infant Crying' ): # "Steady"
            # time1 = time.time()
            vibPwm1.ChangeDutyCycle(50) # continuous and steady vibration alert
            vibPwm2.ChangeDutyCycle(0)
            # time2 = time.time()
            # print(time2 - time1)
            print("IN")
            print("IN")
            print("IN")
            

        elif ( response_data['Alarm'] and response_data['Switch'] and response_data['Label'] == 'Gunshot' ): # Burst
            burst_start_time = time.time()
            print("IN")
            print("IN")
            print("IN")
            
            while ( response_data['Alarm'] and response_data['Switch'] and response_data['Label'] == 'Gunshot' ):
                current_time = time.time()

                if (current_time - burst_start_time <= 0.2):
                    vibPwm1.ChangeDutyCycle(100) # short burst of high-intensity vibration
                    vibPwm2.ChangeDutyCycle(0)
                elif (current_time - burst_start_time <= 0.4):
                    vibPwm1.ChangeDutyCycle(0)
                    vibPwm2.ChangeDutyCycle(0)
                elif (current_time - burst_start_time <= 0.6):
                    vibPwm1.ChangeDutyCycle(100)
                    vibPwm2.ChangeDutyCycle(0)        
                elif (current_time - burst_start_time <= 0.8):
                    vibPwm1.ChangeDutyCycle(100)
                    vibPwm2.ChangeDutyCycle(0)
                else:
                    vibPwm1.ChangeDutyCycle(0)
                    vibPwm2.ChangeDutyCycle(0)
                    break
            
            time3 = time.time()
            print(time3-burst_start_time)

        elif ( response_data['Alarm'] and response_data['Switch'] and response_data['Label'] == 'Glass' ): # Rise
            rise_start_time = time.time()

            for duty in range(0, 101):
                elapsed_time = time.time() - rise_start_time

                target_time = duty / 100
                
                while elapsed_time < target_time:
                    elapsed_time = time.time() - rise_start_time

                vibPwm1.ChangeDutyCycle(duty)
                vibPwm2.ChangeDutyCycle(0)

        else:
            vibPwm1.ChangeDutyCycle(0)
            vibPwm2.ChangeDutyCycle(0)