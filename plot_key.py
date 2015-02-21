import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import sys
from subprocess import call
from mpl_toolkits.basemap import Basemap
import seaborn as sns
sns.set_style("white")
sns.set_style("whitegrid", {"grid.color":'.8', "grid.linewidth": .5})
#sns.axes_style("whitegrid")
#sns.set_context('talk')
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

moisture_stns = ['KLCH', 'KCRP', '76692', 'KTLH', 'KLIX', 'KBRO'] 
lapse_rate_stns = ['KABQ', 'KEPZ', 'KAMA', 'KDNR', 'KMAF', 'KRIW']
lapse_rate_stns = ['KAMA', 'KRIW', 'KEPZ', 'KMAF', 'KABQ', 'KDNR']
stns = lapse_rate_stns
dates = []
sns.palplot(sns.color_palette("cubehelix", 8))
moisture_data = {}
lapse_data = {}
plt.figure(figsize=(7,7))
ax = plt.gca()
m = Basemap(llcrnrlon=-120.0,llcrnrlat=1.,urcrnrlon=-60.566,urcrnrlat=43.352,\
                            rsphere=(6378137.00,6356752.3142),\
                                        resolution='l',area_thresh=1000.,projection='lcc',\
                                                    lat_1=50.,lon_0=-107.,ax=ax)
m.drawcoastlines()
m.drawcountries()
m.drawstates()
data = np.loadtxt('2015021712.csv', delimiter=',', dtype=str)
plt.title("Lapse Rate Ingredient Source Points")
for ma in stns:
    idx = np.where((ma == np.asarray(data[:,0], dtype=str)) & (np.asarray(data[:,5], dtype=int) == 850))[0]
    #datum = data[idx,7]
    print data[idx]
    lat = float(data[idx,2][0])
    lon = float(data[idx,3][0])
    x,y = m(lon, lat)
    plt.plot(x,y, 'o')
plt.show()
 
