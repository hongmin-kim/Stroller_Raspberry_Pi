### RASPBERRY PI, USB MICROPHONE, VIBRATING MOTOR ###
import pyaudio
import wave # read and write audio data in WAV format
import requests # send HTTPS requests and handle responses
import io # used to create an in-memory buffer
#from LED import *
from HANDLE_VIB import *
import time

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

# 오디오 녹음 설정
# each sample: 16-bit binary number. "16-bit" specifies bit depth, related to audio quality and required processing power.
FORMAT = pyaudio.paInt16 # run a test with paInt32
CHANNELS = 1 # mono-recording, instead of stereo.
RATE = 16000 # sample rate in Hz (in accordance with ML server)
# 44100Hz is more suitable for high quality auido tasks, but 16000Hz is sufficient to capture natural speech and computationally economical.
CHUNK = 1000 # number of bytes of audio data read at a time <-- 3.84seconds
ONE_SEC_CHUNKS = 16
# Duration of CHUNK = (# of samples in a CHUNK) / (sample rate) = 0.0625s
# Smaller CHUNK: reduced latency but increased computing needed.
TIME = 10
# This variable is for real-time processing and efficiency
MAX_CHUNKS = 16*TIME # <-- to pack 10 seconds of sound

audio = pyaudio.PyAudio() # an instance of the PyAudio class
audio_chunks = [] # store and manage audio data before sending

def convert_and_send_audio():
    buffer = io.BytesIO() # used to hold WAV file before sending to server
    with wave.open(buffer, 'wb') as wf: # open a WAV file for writing with in the buffer
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT)) # data storage accuracy
        wf.setframerate(RATE)
        wf.writeframes(b''.join(audio_chunks)) # b'': empty bytes object. Concatenate audio data chunks into a single byte.

    audio_data = buffer.getvalue() # Extract audio data written in buffer
    headers = {'Content-Type': 'audio/wav'}
    # http://<서버의 IP 또는 도메인>:3000/uint
    response = requests.post("http://172.20.10.2:3000/uint", data=audio_data, headers=headers)
    # response = requests.post("http://localhost:3000/uint", data=audio_data, headers=headers)
    return response.json()

def record_and_send():
	# Configure and start an audio stream(=recording)
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    while True:
        start_time = time.time()
		# Every loop, "stream" object reads 1024 bytes of audio and stores in audio_chunks
        for i in range(ONE_SEC_CHUNKS):
            data = stream.read(CHUNK)
            audio_chunks.append(data)
        
        # Help manage memory usage
        if len(audio_chunks) > MAX_CHUNKS:
            for i in range(ONE_SEC_CHUNKS):
                audio_chunks.pop(0)

        response_data = convert_and_send_audio()
        receive_time = time.time()
        # LED_alarm(response_data)
        VIB_alarm(response_data)
        print(response_data)
        print("elapsed:{}".format(receive_time - start_time))

    stream.stop_stream()
    stream.close()
    audio.terminate

if __name__ == "__main__":   
    record_and_send()