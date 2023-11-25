import neopixel
import board
import time

num_pixels = 8

def alarm_led_neopixel(response_que_led):
    # Pin Definiiton
    num_pixels = 8
    pixels = neopixel.NeoPixel(board.D18, num_pixels)

    # Parse sound classification result arriving from server
    # response_data ex: {'Alarm': False, 'Label': 'Infant Crying', 'Tagging_rate': 0.00, 'Switch': True}
    while True:
        response_data = response_que_led.get() # retrieve data from the queue. Waits for data to arrive in real-time.
        
        if ( response_data['Alarm'] and response_data['Switch'] and response_data['Label'] == 'Infant Crying' ):
            pixels.fill((0, 255, 0))
        
        elif ( response_data['Alarm'] and response_data['Switch'] and response_data['Label'] == 'Car horn' ):
            yellow_start_time = time.time()

            while ( response_data['Alarm'] and response_data['Switch'] and response_data['Label'] == 'Car horn' ):
                current_time = time.time()

                if (current_time - yellow_start_time <= 0.2):
                    pixels.fill((255, 210, 0))
                elif (current_time - yellow_start_time <= 0.4):
                    pixels.fill((0, 0, 0))
                elif (current_time - yellow_start_time <= 0.6):
                    pixels.fill((255, 210, 0))                    
                elif (current_time - yellow_start_time <= 0.8):
                    pixels.fill((255, 210, 0))
                else:
                    pixels.fill((0, 0, 0))
                    break 

        elif ( response_data['Alarm'] and response_data['Switch'] and response_data['Label'] == 'Siren' ):
            rotate_red(0.0625, 2)

        else:
            pixels.fill((0, 0, 0))

def alarm_led_neopixel_debug(response_queue_led):
    while True:
        response_data = response_queue_led.get()

        if ( response_data['Alarm'] and response_data['Switch'] and response_data['Label'] == 'Infant Crying' ):
            print("LED_'Infant Crying'")

        elif ( response_data['Alarm'] and response_data['Switch'] and response_data['Label'] == 'Car horn' ):
            print("LED_'Gunshot'")

        elif ( response_data['Alarm'] and response_data['Switch'] and response_data['Label'] == 'Glass' ):
            print("LED_'Glass'")

def rotate_red(duration, repeat):
    pixels = neopixel.NeoPixel(board.D18, num_pixels)

    for _ in range(repeat):
        for i in range(num_pixels):
            pixels.fill((0, 0, 0))  # Turn off all pixels
            pixels[i] = (255, 0, 0)  # Set the current pixel to red
            # pixels[(i+4)%num_pixels] = (255, 0, 0)
            pixels.show()
            time.sleep(duration)
        pixels.fill((0, 0, 0))  # Turn off all pixels at the end of a cycle
        pixels.show()