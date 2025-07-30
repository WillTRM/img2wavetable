from PIL import Image
import numpy as np
import wave
import sys
import struct

image_path = str(sys.argv[1])
sample_list = []

image_size = 256

print("Parsing image") #
with Image.open(image_path) as im:
    image_size = im.size[0]
    im = im.resize((image_size, image_size))
    im = im.convert("L")
    for y in range(image_size):
        for x in range(image_size):
            pixel = im.getpixel((x, y))
            sample_list.append(pixel)

print("Rotating image") #
samples = np.array(sample_list)
samples = np.reshape(samples, (image_size, image_size))
samples = np.flip(samples, axis = 0)
samples = samples.flatten()

print("Writing to file") #
with wave.open("out.wav", "w") as wavfile:  
    wavfile.setnchannels(1)
    wavfile.setsampwidth(2)
    wavfile.setframerate(44100)
    for sample in samples:
        sample = int((sample / 255) * 65535 - 32768) # convert to correct range
        wavfile.writeframes(struct.pack("<h", sample))

print("File written!") #
print(f"Window size: {image_size}")