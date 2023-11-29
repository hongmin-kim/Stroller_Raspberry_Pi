### RASPBERRY PI, USB MICROPHONE, ECCENTRIC ROTATING MASS MOTOR ###
import pyaudio
import wave # used to read and write audio data in WAV format
import requests # send HTTPS requests and handle responses
import io # used to create an in-memory buffer
import time
import json
import multiprocessing
import numpy as np
from HANDLE_VIB import alarm_vibration, alarm_vibration_debug
#from LED import alarm_led, alarm_led_debug
from LED_NeoPixel import alarm_led_neopixel, alarm_led_neopixel_debug
# import matplotlib.pyplot as plt
    

# Provide a list of available audio device on my system, their IDs, and their names. 
def list_audio_devices():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')
    
    for i in range(num_devices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        print(f"Device ID: {i}, Name: {device_info.get('name')}")

    p.terminate()

list_audio_devices()

# Audio Recording Settings
# FORMAT: Specifies bit depth of each sample. Related to audio quality and required processing power.
# CHANNELS: 1 = mono-recording.
# RATE: Sample rate in Hz (in accordance with ML server). 16000Hz is sufficient to capture natural speech and is computationally economical.
# CHUNK: Number of bytes of audio data read at a time. Smaller CHUNK reduces latency but increases computing needed.
#        Duration of CHUNK = (# of samples in a CHUNK) / (sample rate) = 0.0625s.
# MAX_CHUNKS: Packs 10 seconds of sound for real-time processing efficiency
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1000
ONE_SEC_CHUNKS = 16
TIME = 5
MAX_CHUNKS = 16 * TIME

# ============== hyperparameter ==============
base_url = "http://172.20.10.2"
motor_debug = False
led_debug = False




audio = pyaudio.PyAudio() # An instance of the PyAudio class
audio_chunks = [] # Store and manage audio data before sending

def calculate_decibels(data):
    data_flatten = np.frombuffer(data, dtype=np.int16)
    data_flatten = data_flatten.astype(np.float32)
    rms = np.sqrt(np.mean(data_flatten ** 2))
    # plt.figure(figsize=(10,4))
    # plt.plot(data_flatten)
    # plt.savefig("temp.jpg")
    decibels = 20 * np.log10(rms)
    return decibels

def post_audio_and_receive_response():
    buffer = io.BytesIO() # Holds WAV file before sending to server
    with wave.open(buffer, 'wb') as wf: # Open a WAV file for writing with in the buffer
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT)) # Accurately store data
        wf.setframerate(RATE)
        wf.writeframes(b''.join(audio_chunks)) # Concatenate audio data chunks into a single byte in an empty bytes object.

    audio_data = buffer.getvalue() # Extract audio data written in buffer

    headers = {'Content-Type': 'application/json'}
    recent_audio_data = b''.join(audio_chunks[-ONE_SEC_CHUNKS:])
    decibel_level = calculate_decibels(recent_audio_data)
    decibel_level = {
        "decibels": decibel_level,
    }
    print(decibel_level)
    json_data = json.dumps(decibel_level)
    requests.post(f"{base_url}:3000/send_decibel", data=json_data, headers=headers)
    
    headers = {'Content-Type': 'audio/wav'}
    # http://<Server IP or domain>:3000/uint
    response = requests.post(f"{base_url}:3000/uint", data=audio_data, headers=headers)
    # response = requests.post("http://localhost:3000/uint", data=audio_data, headers=headers)
    # print(response)
    return response.json()

def record_audio_and_present_response(response_queue_vib, response_queue_led):
	# Configure and start an audio stream(=recording)
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    while True:
        start_time = time.time()
		# Every loop, "stream" object reads 1000 bytes of audio and stores in audio_chunks
        for i in range(ONE_SEC_CHUNKS):
            data = stream.read(CHUNK)
            audio_chunks.append(data)
        
        # Help manage memory usage
        if len(audio_chunks) > MAX_CHUNKS:
            for i in range(ONE_SEC_CHUNKS):
                audio_chunks.pop(0)

        print("--------------------- Result ---------------------")
        response_data = post_audio_and_receive_response()
        response_queue_vib.put(response_data) # insert data into the vib queue.
        response_queue_led.put(response_data) # insert data into the led queue.

        receive_time = time.time()
        print(response_data)
        print("elapsed:{}".format(receive_time - start_time))

    # Unneccessary for live streaming
    # stream.stop_stream()
    # stream.close()
    # audio.terminate

if __name__ == "__main__":


    response_queue_vib = multiprocessing.Queue() # Inter-Process Communication: "Queue" to pass "response_data" to "alarm_vibration()"
    response_queue_led = multiprocessing.Queue()
    if motor_debug == True:
        vib_motor_process = multiprocessing.Process(target=alarm_vibration_debug, args=(response_queue_vib, )) # Create a new process dedicated to vibration
        vib_motor_process.start() # Initiate a separate process and begin executing the target function. Parallel execution in a separate memory space.
    else:
        vib_motor_process = multiprocessing.Process(target=alarm_vibration, args=(response_queue_vib, )) # Create a new process dedicated to vibration
        vib_motor_process.start() # Initiate a separate process and begin executing the target function. Parallel execution in a separate memory space.
    if led_debug == True:
        led_process = multiprocessing.Process(target=alarm_led_neopixel_debug, args=(response_queue_led, ))
        led_process.start()
    else:
        led_process = multiprocessing.Process(target=alarm_led_neopixel, args=(response_queue_led, ))
        led_process.start()

    record_audio_and_present_response(response_queue_vib, response_queue_led)