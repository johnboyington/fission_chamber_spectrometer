import pickle
import numpy as np
import matplotlib.pyplot as plt
from master_data import data_path
from flux import select_flux_spectrum
from unfold import integral_response
from response import generate_responses
from master_data import isos, img_directory
from spectrum import Spectrum


# load in response dict
name = 'test_wims69_resp.p'
resp = pickle.load(open(name, 'rb'))
R = integral_response(name)
RF = resp['response']
for key, val in RF.items():
    RF[key] = val[::-1]

phi_ref = resp['phi'][::-1]
phi_ref = phi_ref / sum(phi_ref)
eb = resp['eb'][::-1] * 1e-6
print(eb)

spectra = {}
spectra['def_spec'] = Spectrum(eb, phi_ref)

# process umg_data
with open(data_path + 'umg_data.p', 'rb') as F:
    umg_data = pickle.load(F)

for key, value in umg_data.items():
    spectra[key] = value[0].solution
    spectra[key].edges

# process roberts data
with open(data_path + 'unfolded_data.p', 'rb') as F:
    unfolded_data = pickle.load(F)

for key, value in unfolded_data.items():
    spectra[key] = Spectrum(eb, value)

## calculate e_avg discrepency
#ft_cutoff = 0.1
#def_e = spectra['def_spec'].e_avg()
#def_ft = spectra['def_spec'].calc_r_tot_ratio(ft_cutoff)
#
#methods = ['shannon', 'hi_shannon', 'low_shannon', '01_tik', '001_tik',
#           'on_mx', 'on_gr', 'hi_mx', 'hi_gr', 'low_mx', 'low_gr',
#           'ones_mx', 'ones_gr']
#e_avg = np.empty((len(methods), 7))
#ft_avg = np.empty((len(methods), 7))
#
#for i, method in enumerate(methods):
#    for j in range(7):
#        key = 'wims69_{}_iso{}'.format(method, j+1)
#        spec_e = spectra[key].e_avg()
#        spec_ft = spectra[key].calc_r_tot_ratio(ft_cutoff)
#        e_avg[i, j] = abs(np.log(spec_e / def_e))
#        ft_avg[i, j] = abs(spec_ft - def_ft) / def_ft
#        # print(def_e, spec_e)
#
#
## plotting
#fig = plt.figure(0)
#ax = fig.add_subplot(111)
#ax.set_xlabel('Isotope Group')
#ax.set_ylabel('Method')
#ax.set_xticks(np.arange(7))
#ax.set_xticklabels(np.arange(7) + 1)
#ax.set_yticks(range(len(methods)))
#ax.set_yticklabels(methods)
#
#image = ax.imshow(e_avg)
#
#plt.colorbar(image)
#
## plotting ft
#fig = plt.figure(1)
#ax = fig.add_subplot(111)
#ax.set_xlabel('Isotope Group')
#ax.set_ylabel('Method')
#ax.set_xticks(np.arange(7))
#ax.set_xticklabels(np.arange(7) + 1)
#ax.set_yticks(range(len(methods)))
#ax.set_yticklabels(methods)
#
#image = ax.imshow(ft_avg)
#
#plt.colorbar(image)

# plot it all
fig = plt.figure(2)
ax = fig.add_subplot(111)
ax.set_xscale('log')
ax.set_yscale('log')


for key, value in spectra.items():
    if 'low_shannon' in key:
        ax.plot(*value.step)
