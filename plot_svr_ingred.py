import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import sys
from subprocess import call
import seaborn as sns
sns.set_style("white")
sns.set_style("whitegrid", {"grid.color":'.8', "grid.linewidth": .5})

def win(wordlist, word_fragment):
    boolean = []
    for w in wordlist:
        boolean.append(w.startswith(word_fragment))
    return boolean

now = datetime.utcnow()
now = now.replace(hour=12)
now = now.replace(minute=0)
now = now.replace(second=0)

delta = timedelta(seconds=(60*60*12))
days = 14
days_delta = timedelta(seconds=(60*60*24*days))
lower_bnd = now - days_delta

# 76595 - MMUN Cancun
# 76644 - MMMD Merida Intl Arpt
# 76692 - MMVR Veracruz
moisture_stns = ['MMMD', '76692', 'KBRO', 'KCRP', 'KLCH', 'KLIX', 'KTLH'] 
lapse_rate_stns = ['KABQ', 'KEPZ', 'KAMA', 'KDNR', 'KMAF', 'KRIW']

#moisture_stns = ["KOAX", "KRAP", "KBIS", "KLBF", "KABR"] 
#lapse_rate_stns = moisture_stns

dates = []
sns.color_palette("cubehelix", 8)
moisture_data = {}
lapse_data = {}
while now >= lower_bnd:
    hour = datetime.strftime(lower_bnd, '%H')
    yyyymmdd = datetime.strftime(lower_bnd, '%Y%m%d')
    print yyyymmdd + hour 
    try:
        data = np.loadtxt(yyyymmdd + hour + '.csv', delimiter=',', dtype=str)
    except:
        print "COULDN'T OPEN:", yyyymmdd+hour+'.csv'
        lower_bnd = lower_bnd + delta
        continue

    for m in moisture_stns:
        idx = np.where((m == np.asarray(data[:,0], dtype=str)) & (np.asarray(data[:,5], dtype=int) == 850))[0]
        datum = data[idx,7]
        print datum
        if len(datum) == 0:
            datum = ['--']
        print datum
        try:
            moisture_data[m] = moisture_data[m] + [datum]
        except:
            moisture_data[m] = [datum]

    for m in lapse_rate_stns:
        idx7 = np.where((m == np.asarray(data[:,0], dtype=str)) & (np.asarray(data[:,5], dtype=int) == 700))[0]
        idx5 = np.where((m == np.asarray(data[:,0], dtype=str)) & (np.asarray(data[:,5], dtype=int) == 500))[0]
        temp7 = data[idx7,6]
        temp5 = data[idx5,6]
        hght7 = data[idx7,8]
        hght5 = data[idx5,8]
        if len(temp7) == 0 or len(temp5) == 0 or len(hght7) == 0 or len(hght5) == 0:
            lapse = ['--']
        else:
            lapse = [(float(temp5[0]) - float(temp7[0]))/(float(hght5[0]) - float(hght7[0])) * 1000.]
        try:
            lapse_data[m] = lapse_data[m] + lapse
        except:
            lapse_data[m] = lapse

    dates.append(lower_bnd)    
    lower_bnd = lower_bnd + delta
    #print data
print lapse_data
fig = plt.figure(figsize=(10,8))
for k in moisture_data.keys():
    print moisture_data[k]
    dat = list(np.asarray(moisture_data[k], dtype=str).squeeze())
    print win(dat, '--')
    invalid = win(dat, '--')
    print np.where(invalid)
    if len( np.where(invalid)[0]) > 0:
        print len(np.where(invalid)[0])
        print dat
        for i in np.where(invalid)[0]:    
            dat[i] = '-9999'
        dat = np.ma.asarray(dat, dtype=float)
        dat = np.ma.masked_where(dat == -9999, dat)
    else:
    #print dat, dates
        dat = np.ma.asarray(dat, dtype=float)
    if len(dat) == len(dates):
        print dat, dates
        print len(dat), len(dates)
        plt.subplot(211)
        plt.plot(np.asarray(dates), dat, 'o-', label=k) 
plt.axhline(y=12.77, color='k', linestyle='.')
plt.title("Severe Wx Thermodynamic Ingredient Source Region Trends", fontsize=15)
plt.legend(loc='upper center', fontsize=10, ncol=6)
plt.ylim(-50,40)
plt.ylabel('850 mb Dew Point [C]')
for k in lapse_data.keys():
    dat = list(np.asarray(lapse_data[k], dtype=str).squeeze())
    invalid = win(dat, '--')
    if np.all(invalid) is True:
        continue

    if len( np.where(invalid)[0]) > 0:
        for i in np.where(invalid)[0]:
            dat[i] = '-9999'
        dat = np.ma.asarray(dat, dtype=float)
        dat = np.ma.masked_where(dat == -9999, dat)
    else:
        dat = np.ma.asarray(dat, dtype=float)

    if len(dat) == len(dates):
        plt.subplot(212)
        plt.plot(np.asarray(dates), -1*dat, 'o-', label=k) 
plt.axhline(y=9.8, color='k', linestyle='.')
plt.ylabel('700-500 mb Lapse Rate [C/km]')
plt.xlabel('Time [UTC]')
plt.ylim(2,10)
fig.autofmt_xdate()
plt.legend(loc='upper center', fontsize=10, ncol=6)
plt.figtext(0, .02, 'Created by Greg Blumberg (OU/CIMMS/SoM)', fontsize=9, transform=plt.gca().transAxes, horizontalalignment='left', verticalalignment='top')
plt.tight_layout()
plt.show()
print dates, moisture_data
