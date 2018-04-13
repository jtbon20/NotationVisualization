import sys
from aubio import source, pitch
from audio_util import get_length_sec
from plot import *
import numpy as np

def array_from_text_file(filename, dtype = 'float'):
    filename = os.path.join(os.path.dirname(__file__), filename)
    return array([line.split() for line in open(filename).readlines()],
        dtype = dtype)

if len(sys.argv) < 2:
    print("Usage: %s <filename> [samplerate]" % sys.argv[0])
    sys.exit(1)

filename = sys.argv[1]

downsample = 16
samplerate = 44100 // downsample
if len( sys.argv ) > 2: samplerate = int(sys.argv[2])

hop_s = 512  // downsample # hop size
length = get_length_sec(filename,samplerate,hop_s);
win_s = 4096 // downsample # fft size

#instantiate the aubio object
s = source(filename, samplerate, hop_s)

tolerance = 0.7
pitch_o = pitch("yin", win_s, hop_s, samplerate)
pitch_o.set_unit("midi")
pitch_o.set_unit("midi")
pitch_o.set_tolerance(tolerance)

pitches = []
times = []
confidences = []

# total number of frames read
total_frames = 0
while True:
    #Sample and determine pitch with confidences
    samples, read = s()
    pitch = pitch_o(samples)[0]
    confidence = pitch_o.get_confidence()

    #save resulting data
    pitches += [pitch]
    times += [total_frames]
    confidences += [confidence]
    total_frames += read
    if read < hop_s: break

import os.path
from numpy import array, ma
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from demo_waveform_plot import get_waveform_plot, set_xlabels_sample2time

skip = 1
pitches = array(pitches[skip:])
confidences = array(confidences[skip:])
times = [t * hop_s for t in range(len(pitches))]



ground_truth = os.path.splitext(filename)[0] + '.f0.Corrected'
if os.path.isfile(ground_truth):
    ground_truth = array_from_text_file(ground_truth)
    true_freqs = ground_truth[:,2]
    true_freqs = ma.masked_where(true_freqs < 2, true_freqs)
    true_times = float(samplerate) * ground_truth[:,0]
    ax2.plot(true_times, true_freqs, 'r')
    ax2.axis( ymin = 0.9 * true_freqs.min(), ymax = 1.1 * true_freqs.max() )


cleanP = []
cleanT = []

print (max(pitches))

for i in range(1,len(times)):
    if (pitches[i] > 1):
        cleanP+=[pitches[i]]
        cleanT+=[times[i]]

print (min(pitches))

top = 300
bottom = -300

cleaned_pitches = pitches
cleaned_pitches = ma.masked_where(confidences < tolerance, cleaned_pitches)
cleaned_pitches = ma.masked_where(cleaned_pitches > top, cleaned_pitches)
cleaned_pitches = ma.masked_where(cleaned_pitches < bottom, cleaned_pitches)
dta = ma.MaskedArray.compressed(cleaned_pitches)


cleaned_times = times
cleaned_times = ma.masked_where(confidences < tolerance, cleaned_times)
cleaned_times = ma.masked_where(cleaned_pitches > top, cleaned_times)
cleaned_times = ma.masked_where(cleaned_pitches < bottom, cleaned_times)
x = ma.MaskedArray.compressed(cleaned_times)

fig = plt.figure(figsize=(325, 5), dpi=200)
plt.plot(x,dta,c="black", lw=.5)
size = (  dta)**2

plt.scatter(x,dta, c = dta , s = size)
plt.axis('off')

plt.savefig(os.path.basename(filename) + '.svg', bbox_inches='tight')
plt.close();


#n, bins, patches = plt.hist(dta, 50, normed=1, facecolor='green', alpha=0.75)
#plt.savefig(os.path.basename(filename) + '.svg')
