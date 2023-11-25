# import RPi.GPIO as GPIO
# import time
# LED = 18

# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(LED, GPIO.OUT)

# GPIO.output(LED, GPIO.HIGH)
# time.sleep(2)
# GPIO.output(LED, GPIO.LOW)
# GPIO.cleanup()


# import board
# import neopixel
# pixels = neopixel.NeoPixel(board.D18, 30)

# # pixels[0] = (255, 0, 0)
# pixels.fill((0, 255, 0))

# import time
# time.sleep(1)

# # SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# # SPDX-License-Identifier: MIT

# # Simple test for NeoPixels on Raspberry Pi
# import time
# import board
# import neopixel


# # Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# # NeoPixels must be connected to D10, D12, D18 or D21 to work.
# pixel_pin = board.D18

# # The number of NeoPixels
# num_pixels = 8

# # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
# ORDER = neopixel.GRBW

# pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1.0, auto_write=False, pixel_order=ORDER, bpp=4)

# pixels.fill((255, 255, 255, 0))
# pixels.show()
# def wheel(pos):
#     # Input a value 0 to 255 to get a color value.
#     # The colours are a transition r - g - b - back to r.
#     if pos < 0 or pos > 255:
#         r = g = b = 0
#     elif pos < 85:
#         r = int(pos * 3)
#         g = int(255 - pos * 3)
#         b = 0
#     elif pos < 170:
#         pos -= 85
#         r = int(255 - pos * 3)
#         g = 0
#         b = int(pos * 3)
#     else:
#         pos -= 170
#         r = 0
#         g = int(pos * 3)
#         b = int(255 - pos * 3)
#     return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


# def rainbow_cycle(wait):
#     for j in range(255):
#         for i in range(num_pixels):
#             pixel_index = (i * 256 // num_pixels) + j
#             pixels[i] = wheel(pixel_index & 255)
#         pixels.show()
#         time.sleep(wait)


# while True:
#     # Comment this line out if you have RGBW/GRBW NeoPixels
#     pixels.fill((255, 0, 0))
#     # Uncomment this line if you have RGBW/GRBW NeoPixels
#     # pixels.fill((255, 0, 0, 0))
#     pixels.show()
#     time.sleep(1)

#     # Comment this line out if you have RGBW/GRBW NeoPixels
#     pixels.fill((0, 255, 0))
#     # Uncomment this line if you have RGBW/GRBW NeoPixels
#     # pixels.fill((0, 255, 0, 0))
#     pixels.show()
#     time.sleep(1)

#     # Comment this line out if you have RGBW/GRBW NeoPixels
#     pixels.fill((0, 0, 255))
#     # Uncomment this line if you have RGBW/GRBW NeoPixels
#     # pixels.fill((0, 0, 255, 0))
#     pixels.show()
#     time.sleep(1)

#     rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step

# import RPi.GPIO as GPIO
# import time
# GPIO.setwarnings(False)

# GPIO.setmode(GPIO.BCM)
# led_pin = 18  # Replace with your LED pin number

# GPIO.setup(led_pin, GPIO.OUT)

# try:
#     while True:
#         GPIO.output(led_pin, GPIO.HIGH)
#         time.sleep(1)
#         GPIO.output(led_pin, GPIO.LOW)
#         time.sleep(1)
# except KeyboardInterrupt:
#     GPIO.cleanup()
import neopixel
import board
import time

# RED = 0x100000

pixels = neopixel.NeoPixel(board.D18, 8)
# for i in range(len(pixels)):
#     pixels[i] = RED

pixels.fill((125, 60, 10))
time.sleep(3)
pixels.fill((0, 0, 0))
