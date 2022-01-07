import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import allantools as allantools
# Laser Wavelength Meter: WS8-10
c = 299792458; #speed of light

# Calculate fractional frequency = (f-f_ave)/f_ave
# Laser is locked by a pump beam with low intensity
# The data is read from wavemeter in unit of nm
data0 = pd.read_csv('780_data_without_broadening.csv')
time1=data0['Time  [ms]'].values
data1=data0['Wavelength [nm]'].values
# convert wavelenght to frequency
data1=c/(data1*1e-9); # frequency at time t
ave_data1=np.mean(data1); # average frequency
data_frac1=(data1-ave_data1)/ave_data1;

# Calculate fractional frequency = (f-f_ave)/f_ave
# Laser is locked by a pump beam with high intensity
# The data is read from wavemeter in unit of nm
data0 = pd.read_csv('780_data_broadening.csv')
time2=data0['Time  [ms]'].values
data2=data0['Wavelength [nm]'].values
# convert wavelenght to frequency
data2=c/(data2*1e-9); # frequency at time t
ave_data2=np.mean(data2); # average frequency
data_frac2=(data2-ave_data2)/ave_data2;

# Generate white noise
data_noise = float(data1[0])*(data1*0+1)+np.random.randn(len(data1))*40e3;
ave_data_noise=np.mean(data_noise);
data_frac_noise =(data_noise -ave_data_noise)/ave_data_noise 

n = 100000
taus0 = np.linspace(1,n,n)
(t1, ad1, ade1, adn1) = allantools.adev(data_frac1, rate=1, data_type="freq", taus=taus0)
(t2, ad2, ade2, adn2) = allantools.adev(data_frac2, rate=1, data_type="freq", taus=taus0)
(t_noise, ad_noise, ade_noise, adn_noise) = allantools.adev(data_frac_noise, rate=1, data_type="freq", taus=taus0)
plt.figure(1)
plt.plot(t1,ad1, label='Without power broadening')
plt.plot(t2,ad2,'--', label='With power broadening')
plt.plot(t_noise,ad_noise,'--', label='White noise')
plt.legend(loc=3, prop={'size': 24})
plt.xscale("log")
plt.yscale("log")
plt.xlabel('Time (sec)',fontsize=20)
plt.ylabel('Allan Deviation',fontsize=20)
plt.xticks(fontsize=18 )
plt.yticks(fontsize=20 )

plt.figure(2)
index1 = time1<20*(1e3*60)
index2 = time2<20*(1e3*60)
time1 = time1[index1]/(60*1e3)
time2 = time2[index2]/(60*1e3)
data1 = data1[index1]/1e12
data2 = data2[index2]/1e12
plt.plot(time2,data2,'--')
plt.plot(time1,data1,'r')
plt.xlabel('Time (mins)',fontsize=20)
plt.ylabel('Frequency (THz)',fontsize=20)
plt.xticks(fontsize=20 )
plt.yticks(fontsize=20 )
