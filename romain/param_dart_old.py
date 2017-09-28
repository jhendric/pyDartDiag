# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 10:59:19 2016

@author: romain
"""

import numpy as np
import netCDF4 as ncdf
import datetime as dtime
import os
import rt_plotbox
import rt_dart_tools
import matplotlib.pylab as plt
import matplotlib.cm as cm
import matplotlib.dates as mpl_dates
import os.path
import glob
import rt_netcdf_tools
import rt_roms_tools

plt.close('all')
rt_colormaps = rt_plotbox.rt_getcolormaps()
rt_colors = rt_plotbox.rt_getcolors()

#%% Parameters

geo = [-98, -45, 10, 52]
simu= 'NWA-RE.REANA45'
N_members = 30

# Period
period = {
        'NWA-RE.REANA04': [dtime.datetime(2011,1,1),dtime.datetime(2011,1,10),dtime.datetime(2011,3,5)],
        'NWA-RE.REANA22': [dtime.datetime(2011,1,1),dtime.datetime(2011,1,3),dtime.datetime(2011,1,15)],
        'NWA-RE.REANA24': [dtime.datetime(2011,1,1),dtime.datetime(2011,1,3),dtime.datetime(2011,3,2)],
        'NWA-RE.REANA25': [dtime.datetime(2011,1,1),dtime.datetime(2011,1,2),dtime.datetime(2011,1,16)],
        'NWA-RE.REANA26': [dtime.datetime(2011,1,1),dtime.datetime(2011,1,16),dtime.datetime(2011,1,23)],
        'NWA-RE.REANA27': [dtime.datetime(2011,1,1),dtime.datetime(2011,1,16),dtime.datetime(2011,2,12)],
        'NWA-RE.REANA28': [dtime.datetime(2011,1,1),dtime.datetime(2011,1,16),dtime.datetime(2011,3,2)],
        'NWA-RE.REANA29': [dtime.datetime(2011,1,1),dtime.datetime(2011,1,16),dtime.datetime(2011,4,26)],
        'NWA-RE.REANA30': [dtime.datetime(2011,1,1),dtime.datetime(2011,3,22),dtime.datetime(2011,5,31)],
        'NWA-RE.REANA31': [dtime.datetime(2011,1,1),dtime.datetime(2011,3,22),dtime.datetime(2011,5,27)],
        'NWA-RE.REANA32': [dtime.datetime(2011,1,1),dtime.datetime(2011,2,21),dtime.datetime(2011,3,6)],
        'NWA-RE.REANA36': [dtime.datetime(2010,9,1),dtime.datetime(2011,1,2),dtime.datetime(2011,5,9)],
        'NWA-RE.REANA37': [dtime.datetime(2010,9,1),dtime.datetime(2011,1,2),dtime.datetime(2011,2,28)],
        'NWA-RE.REANA38': [dtime.datetime(2010,9,1),dtime.datetime(2011,6,2),dtime.datetime(2011,1,4)],
        'NWA-RE.REANA39': [dtime.datetime(2010,9,1),dtime.datetime(2011,6,1),dtime.datetime(2011,2,28)],
        'NWA-RE.REANA40': [dtime.datetime(2010,9,1),dtime.datetime(2011,1,2),dtime.datetime(2011,4,4)],
        'NWA-RE.REANA41': [dtime.datetime(2010,7,1),dtime.datetime(2011,1,2),dtime.datetime(2011,12,31)],
        'NWA-RE.REANA44': [dtime.datetime(2010,7,1),dtime.datetime(2011,1,2),dtime.datetime(2011,11,19)],
        'NWA-RE.REANA45': [dtime.datetime(2010,7,1),dtime.datetime(2011,1,2),dtime.datetime(2011,1,16)],
}[simu]
start_simu  = period[0]
#start_assim = dtime.datetime(2011,1,16)
start_assim = period[1]
final_assim = period[2]
N_days = (final_assim-start_assim).days+1
N_days_simu = (final_assim-start_simu).days+1
datevec_assim=[start_assim+dtime.timedelta(i_date) for i_date in range(N_days)]
datevec_simu=[start_simu+dtime.timedelta(i_date) for i_date in range(N_days_simu)]
date_step=max(1,int(np.ceil(N_days/5.)))

yearvec_simu = np.arange(start_simu.year,final_assim.year+1)
datevec_simu_month = []
for year_tmp in yearvec_simu:
   if (year_tmp == yearvec_simu[0]):
      start_month = start_simu.month
   else:
      start_month = 1
   if (year_tmp == yearvec_simu[-1]):
      final_month = final_assim.month
   else:
      final_month = 12
   for month_tmp in np.arange(start_month,final_month+1):
      datevec_simu_month.append(dtime.datetime(year_tmp,month_tmp,1))




# Directories
dir_simu= '/Users/romain/Work/Projects/Dart/Data/' + simu + '/'
#dir_simu = '/Volumes/P11/DART/tmpdir_' + simu + '/'
dir_simu = dir_data + simu + '/'
dir_obs  = dir_simu + 'ObsOut/'
dir_diag = dir_simu + 'Diags/'
dir_pictures = dir_simu + 'Pictures/'
if not os.path.exists(dir_pictures):
    os.makedirs(dir_pictures)
dir_postprod = dir_simu + 'PostProd/'
if not os.path.exists(dir_postprod):
    os.makedirs(dir_postprod)
dir_average = dir_simu + 'Outputs/Average/'


# Grid
file_grid = ${dir_simu%/*/} + '/NWA_grd_newwtypechl.nc'
RomsGrid = rt_roms_tools.romsGrid(file_grid)
RomsGrid.get_grid()
RomsGrid.get_std_depths()

# Diagnostics
copy = ['Prior','Analysis']
var_type = ['SATELLITE_SST','T_PROFILES','S_PROFILES','SATELLITE_SLA']
var_id   = [52,16,15,[i for i in xrange(56,70)]]
sel_type = [3]
layer = [(0,5000),(0,10),(10,100),(100,500),(500,1000),(1000,5000)]

