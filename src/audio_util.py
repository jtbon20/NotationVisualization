import sys
from aubio import source
from numpy import array, ma, zeros, hstack

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

def get_reshaped_energy_data( filename, samplerate = 1, block_size = 4096, downsample = 1):
    hop_s = block_size
    allsamples_max = zeros(0,)

    a = source(filename, samplerate, hop_s)            # source file
    if samplerate == 0: samplerate = a.samplerate

    total_frames = 0

    while True:
        samples, read = a()
        # keep some data to plot it later
        new_maxes = (abs(samples.reshape(hop_s//downsample, downsample))).max(axis=0)
        allsamples_max = hstack([allsamples_max, new_maxes])
        total_frames += read
        if read < hop_s: break

    allsamples_max = (allsamples_max > 0) * allsamples_max
    allsamples_max_times = [ ( float (t) / downsample ) * hop_s for t in range(len(allsamples_max)) ]
    return    (allsamples_max, allsamples_max_times)
