import sys
from aubio import source

#Run through song, get length in seconds
def get_length_sec(filename, samplerate = 512, hop_size = 256):

    f = source(filename, samplerate, hop_size)

    total_frames, read = 0, f.hop_size

    while read:
        vec, read = f()
        total_frames += read
        if read < f.hop_size: break

    return total_frames / float(samplerate);

def get_length_frames(filename, samplerate = 512, hop_size = 256):
    f = source(filename, samplerate, hop_size)

    total_frames, read = 0, f.hop_size

    while read:
        vec, read = f()
        total_frames += read
        if read < f.hop_size: break

    return total_frames
