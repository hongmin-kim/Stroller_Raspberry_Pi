import pyaudio
import wave # read and write audio data in WAV format
import requests # send HTTPS requests and handle responses
import io # used to create an in-memory buffer

# 오디오 녹음 설정
# each sample: 16-bit binary number. "16-bit" specifies bit depth, related to audio quality and required processing power.
FORMAT = pyaudio.paInt16 # run a test with paInt32
CHANNELS = 1 # mono-recording, instead of stereo.
RATE = 16000 # sample rate in Hz (in accordance with ML server)
CHUNK = 1024 # number of bytes of audio data read at a time <-- 3.84seconds
# Duration of CHUNK = (# of samples in a CHUNK) / (sample rate) = 0.064s
# Smaller CHUNK: reduced latency but increased computing needed.
# This variable is for real-time processing and efficiency
MAX_CHUNKS = 60

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
    headers = {'Content-Type': 'application/octet-stream'}
    # http://<서버의 IP 또는 도메인>:3000/uint
    response = requests.post("http://172.20.10.5:3000/uint", data=audio_data, headers=headers)
    return response.json()

def record_and_send():
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    while True:
        data = stream.read(CHUNK)
        audio_chunks.append(data)
        
        # 청크의 수가 60을 초과하면 가장 오래된 청크 제거
        if len(audio_chunks) > MAX_CHUNKS:
            audio_chunks.pop(0)

        response_data = convert_and_send_audio()
        print(response_data)

    stream.stop_stream()
    stream.close()
    audio.terminate

if __name__ == "__main__":   
    record_and_send()