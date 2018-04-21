from pydub import AudioSegment

sound = AudioSegment.from_mp3("v1.mp3")

# get raw audio data as a bytestring
rawData = sound.raw_data
# get the frame rate
sampleRate = sound.frame_rate
# get amount of bytes contained in one sample
sampleSize = sound.sample_width
# get channels
channels = sound.channels

print(sampleRate, sampleSize, channels)