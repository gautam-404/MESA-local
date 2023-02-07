from astropy.stats import LombScargle
from astropy.convolution import convolve, Box1DKernel
import matplotlib.pyplot as plt
import numpy as np
from lightkurve import search_lightcurve
import pandas as pd
import scipy as sp


def get_PDC_lightcurve(target, **kwargs):
    lc_collection = search_lightcurve(target, **kwargs).download_all()

    lc = lc_collection[0].PDCSAP_FLUX.normalize()
    for l in lc_collection[1:]:
        lc = lc.append(l.PDCSAP_FLUX.normalize())

    lc = lc.remove_nans()
    magnitude = -2.5 * np.log10(lc.flux)
    magnitude = magnitude - np.average(magnitude)
    return lc.time.value, magnitude.value


def amp_spectrum(t, y, fmin=None, fmax=None, nyq_mult=1., oversample_factor=5.):
    tmax = t.max()
    tmin = t.min()
    df = 1.0 / (tmax - tmin)
    
    if fmin is None:
        fmin = df
    if fmax is None:
        fmax = (0.5 / np.median(np.diff(t)))*nyq_mult

    freq = np.arange(fmin, fmax, df / oversample_factor)
    model = LombScargle(t, y)
    sc = model.power(freq, method="fast", normalization="psd")

    fct = np.sqrt(4./len(t))
    amp = np.sqrt(sc) * fct

    return freq, amp


t,m = get_PDC_lightcurve("HD31901",mission="TESS",cadence=120,author="SPOC")
np.savetxt("stars/hd31901_lk.csv",np.array([t,m]).T)
f,a = amp_spectrum(t,m,fmax=90)
amp2=convolve(a, Box1DKernel(20))

plt.plot(f,amp2,c='k')
plt.ylim(bottom=0)
plt.xlim(left=0)
plt.xlabel(r"Frequency, d$^{-1}$")
plt.ylabel("Amplitude, mmag")
