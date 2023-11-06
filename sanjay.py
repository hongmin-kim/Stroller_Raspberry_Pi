import pyaudio
import wave

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 5
OUTPUT_FILE = "1024_test.wav"
MAX_CHUNKS = 60

audio = pyaudio.PyAudio()

stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

frames = []

print("Recording...")

for _ in range(0, int(RATE / 1024 * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Finished recording.")

# Save the recorded audio to a WAV file
with wave.open(OUTPUT_FILE, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

# bit_depth_bytes = audio.get_sample_size(FORMAT)
# bit_depth = bit_depth_bytes * 8  # Convert bytes to bits

# print(f"Bit Depth: {bit_depth} bits")

# Clean up
stream.stop_stream()
stream.close()
audio.terminate()

# try:
#     print("Recording...")

#     while True:

#         data = stream.read(CHUNK)
#         frames.append(data)

#         if len(frames) > MAX_CHUNKS:
#             frames.pop(0)

# except KeyboardInterrupt:
#     print("Finished Recording")
