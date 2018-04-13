import sys
from aubio import source
from numpy import array, ma

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


def filter_array(array, confidences, tolerance, top=120, bottom=0):
    cleaned = array

    #Mask based on parameters
    cleaned = ma.masked_where(confidences < tolerance, cleaned)
    cleaned = ma.masked_where(cleaned > top, cleaned)
    cleaned = ma.masked_where(cleaned < bottom, cleaned)
    return ma.MaskedArray.compressed(cleaned)

def filter_array_on_other(array, arrayOther, confidences, tolerance, top = 120, bottom = 0):
    cleaned = array

    #Mask based on parameters
    cleaned = ma.masked_where(confidences < tolerance, cleaned)
    cleaned = ma.masked_where(arrayOther > top, cleaned)
    cleaned = ma.masked_where(arrayOther < bottom, cleaned)
    return ma.MaskedArray.compressed(cleaned)
