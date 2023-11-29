import RPi.GPIO as GPIO

def alarm_led(response_queue_led):
    # Pin Definition !!! Needs Update !!!
    LED_R = 26 
    LED_G = 4 
    LED_Y = 5

    # Pin Setting
    GPIO.setmode(GPIO.BOARD) # no breadboard
    GPIO.setup(LED_R, GPIO.OUT)
    GPIO.setup(LED_G, GPIO.OUT)
    GPIO.setup(LED_Y, GPIO.OUT)

    # Parse sound classification result arriving from server
    # response_data ex: {'Alarm': False, 'Label': 'Infant Crying', 'Tagging_rate': 0.00, 'Switch': True}
    while True:
        response_data = response_queue_led.get() # retrieve data from the queue. Waits for data to arrive in real-time.

        if ( response_data['Alarm'] and response_data['Switch'] and response_data['Label'] == 'Infant Crying' ):
            GPIO.output(LED_G, GPIO.HIGH)
            GPIO.output(LED_R, GPIO.LOW)
            GPIO.output(LED_Y, GPIO.LOW)

        elif ( response_data['Alarm'] and response_data['Switch'] and response_data['Label'] == 'Gunshot' ):
            GPIO.output(LED_R, GPIO.HIGH)
            GPIO.output(LED_G, GPIO.LOW)
            GPIO.output(LED_Y, GPIO.LOW)

        elif ( response_data['Alarm'] and response_data['Switch'] and response_data['Label'] == 'Glass' ):
            GPIO.output(LED_Y, GPIO.HIGH)
            GPIO.output(LED_G, GPIO.LOW)
            GPIO.output(LED_R, GPIO.LOW)

        else:
            GPIO.output(LED_R, GPIO.LOW)
            GPIO.output(LED_G, GPIO.LOW)
            GPIO.output(LED_Y, GPIO.LOW)

    # GPIO reset
    GPIO.cleanup()

def alarm_led_debug(response_queue_led):
    while True:
        response_data = response_queue_led.get()

        if ( response_data['Alarm'] and response_data['Switch'] and response_data['Label'] == 'Infant Crying' ):
            print("LED_'Infant Crying'")

        elif ( response_data['Alarm'] and response_data['Switch'] and response_data['Label'] == 'Gunshot' ):
            print("LED_'Gunshot'")

        elif ( response_data['Alarm'] and response_data['Switch'] and response_data['Label'] == 'Glass' ):
            print("LED_'Glass'")

