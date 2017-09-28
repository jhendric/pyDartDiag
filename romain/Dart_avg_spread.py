print('----------------------------------------------------------------')
print('                        Spread of ensemble                      ')
print('----------------------------------------------------------------')

#%% Toolboxes

from param_dart import *

#%%

Prior_avg = dir_obs_diag + 'Avg_Prior_Diag_timeseries.nc4'

nc_prior_avg = ncdf.Dataset(Prior_avg,'r')

spr_temp = nc_prior_avg.variables['temp'][:,1,:]
spr_salt = nc_prior_avg.variables['salt'][:,1,:]
spr_zeta = nc_prior_avg.variables['zeta'][:,1]

nc_prior_avg.close()

limX = mpl_dates.date2num(dtime.datetime(2010,7,1)),mpl_dates.date2num(dtime.datetime(2011,4,1))
disp_period=mpl_dates.num2date(limX[0]).strftime('%Y%m%d')+'_'+mpl_dates.num2date(limX[1]).strftime('%Y%m%d')

datevec = [start_simu+dtime.timedelta(i) for i in xrange(spr_temp.shape[0])]

fds = mpl_dates.date2num(datevec)
datevec_simu.append(datevec_simu[-1]+dtime.timedelta(1))
fds_ext = mpl_dates.date2num(datevec_simu) # converted

fig = plt.figure(figsize=[25.,15.]);plt.clf()
ax1 = fig.add_subplot(3,1,1)
pt = plt.pcolor(fds,np.arange(0,40),spr_temp.transpose(),vmin=0,vmax=0.7,cmap=rt_colormaps['ncview_banded'])
cb = plt.colorbar(); cb.set_label('degC',size=16);cb.ax.tick_params(labelsize=16)
plt.grid()
rt_plotbox.xaxis_date(fds_ext,step='month',date_format='%d %b')
plt.xlim(limX)
ax1.xaxis.set_tick_params(labelsize=16)
ax1.yaxis.set_tick_params(labelsize=16)
ax1.yaxis.set_label_text('depth level',size=16)
plt.title('Spatially averaged temperature spread',fontsize=20)
fig.autofmt_xdate()

ax1 = fig.add_subplot(3,1,2)
pt = plt.pcolor(fds,np.arange(0,41),spr_salt.transpose(),vmin=0,vmax=0.2,cmap=rt_colormaps['ncview_banded'])
cb = plt.colorbar(); cb.set_label('PSU',size=16);cb.ax.tick_params(labelsize=16)
plt.grid()
rt_plotbox.xaxis_date(fds_ext,step='month',date_format='%d %b')
plt.xlim(limX)
ax1.xaxis.set_tick_params(labelsize=16)
ax1.yaxis.set_tick_params(labelsize=16)
ax1.yaxis.set_label_text('depth level',size=16)
plt.title('Spatially averaged salinity spread',fontsize=20)
fig.autofmt_xdate()

ax1 = fig.add_subplot(3,1,3)
plt.plot(fds,spr_zeta*100,linewidth=2)
plt.pcolor(np.ones((2,2)))
plt.xlim(limX)
plt.grid()
rt_plotbox.xaxis_date(fds_ext,step='month',date_format='%d %b')
ax1.xaxis.set_tick_params(labelsize=16)
ax1.yaxis.set_tick_params(labelsize=16)
ax1.yaxis.set_label_text('cm',size=16)
plt.title('Spatially averaged zeta spread',fontsize=20)
fig.autofmt_xdate()
plt.tight_layout()
cb_tmp = plt.colorbar(); cb_tmp.remove()

figname=dir_pictures+'Spread_spatavg_test_'+simu+'_'+disp_period+'.png'
plt.savefig(figname)
print figname







