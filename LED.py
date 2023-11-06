import RPi.GPIO as GPIO

# Pin Definition
LED_R = 26
LED_G = 4
LED_Y = 5

# Pin Setting
GPIO.setmoode(GPIO.BOARD)
GPIO.setup(LED_R, GPIO.OUT)
GPIO.setup(LED_G, GPIO.OUT)
GPIO.setup(LED_Y, GPIO.OUT)

def LED_alarm(response_data):

    # Parse sound classification arriving from server
    # Note that in send_audio.py, response_data is a dictionary
    # Turn LED on if desired sound is detected AND switch for that sound is on
    if ( (response_data['Label'] == 'Infant Crying') and  (response_data['Switch'] == True) ):
        GPIO.output(LED_G, GPIO.HIGH)
        GPIO.output(LED_R, GPIO.LOW)
        GPIO.output(LED_Y, GPIO.LOW)

    elif ( (response_data['Label'] == 'Gunshot') and (response_data['Switch'] == True) ):
        GPIO.output(LED_R, GPIO.HIGH)
        GPIO.output(LED_G, GPIO.LOW)
        GPIO.output(LED_Y, GPIO.LOW)

    elif ( (response_data['Label'] == 'Glass') and (response_data['Switch'] == True) ):
        GPIO.output(LED_Y, GPIO.HIGH)
        GPIO.output(LED_G, GPIO.LOW)
        GPIO.output(LED_R, GPIO.LOW)

    else:
        GPIO.output(LED_R, GPIO.LOW)
        GPIO.output(LED_G, GPIO.LOW)
        GPIO.output(LED_Y, GPIO.LOW)

    # GPIO reset
    GPIO.cleanup()