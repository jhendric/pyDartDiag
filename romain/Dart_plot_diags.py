# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 14:35:27 2016

@author: romain
"""

print('----------------------------------------------------------------')
print('                        Post-processing Obs Dart                ')
print('----------------------------------------------------------------')

#%% Toolboxes

from param_dart import *

#%% Diagnosis

file_obs_diag = dir_obs+'obs_diag_romain.nc'
nc_diags = ncdf.Dataset(file_obs_diag,'r')
date_vec = [dtime.datetime(1900,1,1)+dtime.timedelta(dt) for dt in nc_diags.variables['time'][:]]
fds = mpl_dates.date2num(date_vec) # converted

variname = nc_diags.Variable_type.split(',')[0:-1]
copyname = nc_diags.Copy.split(',')[0:-1]
diagname = [u'RMSE',u'Bias',u'Spread',u'Total Spread']

n_time = len(date_vec)
n_diag = len(diagname)
n_copy = len(copyname)
n_var  = len(variname)

diags_good = np.ma.empty((n_diag,n_copy,n_var,n_time))
diags = np.ma.empty((n_diag,n_copy,n_var,n_time))

diags_good[0,:,:,:] = nc_diags.variables['RMSE_good'][:,:,0,:]
diags_good[1,:,:,:] = nc_diags.variables['Bias_good'][:,:,0,:]
diags_good[2,:,:,:] = nc_diags.variables['Spread_good'][:,:,0,:]
diags_good[3,:,:,:] = nc_diags.variables['TotalSpread_good'][:,:,0,:]

diags[0,:,:,:] = nc_diags.variables['RMSE'][:,:,0,:]
diags[1,:,:,:] = nc_diags.variables['Bias'][:,:,0,:]
diags[2,:,:,:] = nc_diags.variables['Spread'][:,:,0,:]
diags[3,:,:,:] = nc_diags.variables['TotalSpread'][:,:,0,:]

N_QC  = nc_diags.variables['N_obs_QC'][:,0,:,:]
n_var,n_qc,n_time = N_QC.shape

nc_diags.close()

for i_var in xrange(0,n_var):
   fig = plt.figure(figsize=[15.,15.]);plt.clf()
   for i_diag in xrange(0,n_diag):
      # Create a subplot for each diag
      ax1 = fig.add_subplot(2,2,i_diag+1)
      # Plot prior and analysis
      idx_nonmasked=np.ma.MaskedArray.nonzero(diags[i_diag,0,i_var,:].squeeze()) 
      ax1.plot(fds[idx_nonmasked], diags[i_diag,0,i_var,idx_nonmasked].squeeze(), 'k-*',label=copyname[0])
      ax1.plot(fds[idx_nonmasked], diags[i_diag,1,i_var,idx_nonmasked].squeeze(), 'r-*',label=copyname[1])
      ax1.set_ylim(bottom = min(0,np.min(diags[i_diag,0,i_var,:].squeeze())), top = 1.3*np.max(diags[i_diag,0,i_var,:].squeeze()))
      ax1.set_title(diagname[i_diag] + ' all ('+variname[i_var]+')', color='k')
      ax1.set_xlabel('time', color='k')
      rt_plotbox.xaxis_date(fds,ax=ax1,step=date_step,date_format='%m/%d')
      ax1.set_xlim(left=mpl_dates.date2num(start_assim)-1,right=mpl_dates.date2num(final_assim)+1)
      ax1.plot(fds, np.zeros_like(fds),'k--')
      ax1.grid()
      if (i_diag == 0):
         ax1.set_ylim(bottom = min(0,np.min(diags[i_diag,0,i_var,:].squeeze())), top = 1.6*np.max(diags[i_diag,0,i_var,:].squeeze()))
         # Add number of observations assimilated
         ax2 = ax1.twinx()
         ax2.plot(fds, np.sum(N_QC[i_var,:,:],axis=0), 'o', markerfacecolor='w',markeredgecolor='b')
         ax2.plot(fds, N_QC[i_var,0,:].squeeze(), 'b+')
         ax2.set_ylim(bottom = -500, top = 1.1*np.max(np.sum(N_QC[i_var,:,:],axis=0)))
         ax2.set_ylabel('# of obs : o=possible, +=assimilated', color='b')
         ax2.set_xlim(left=mpl_dates.date2num(start_assim)-1,right=mpl_dates.date2num(final_assim)+1)
         for tl in ax2.get_yticklabels():
            tl.set_color('b')
         # Put legend on graph
         h1, l1 = ax1.get_legend_handles_labels()
         ax2.legend(h1,l1,fancybox=True)
   figname=dir_pictures + '/Diags_rt_all_' + simu + '_' + variname[i_var] + '.png'
   plt.tight_layout()
   plt.savefig(figname)
   print(figname)

#   fig = plt.figure(figsize=[15.,15.]);plt.clf()
#   for i_diag in xrange(0,n_diag):
#      # Create a subplot for each diag
#      ax1 = fig.add_subplot(2,2,i_diag+1)
#      # Plot prior and analysis
#      idx_nonmasked=np.ma.MaskedArray.nonzero(diags_good[i_diag,0,i_var,:].squeeze())
#      ax1.plot(fds[idx_nonmasked], diags_good[i_diag,0,i_var,idx_nonmasked].squeeze(), 'k-*',label=copyname[0])
#      ax1.plot(fds[idx_nonmasked], diags_good[i_diag,1,i_var,idx_nonmasked].squeeze(), 'r-*',label=copyname[1])
#      ax1.set_ylim(bottom = min(0,1.1*np.min(diags_good[i_diag,0,i_var,:].squeeze())), top = max(0,1.3*np.max(diags_good[i_diag,0,i_var,:].squeeze())))
#      ax1.set_title(diagname[i_diag] + ' assimilated ('+variname[i_var]+')', color='k')
#      ax1.set_xlabel('time', color='k')
#      rt_plotbox.xaxis_date(fds,ax=ax1,step=date_step,date_format='%m/%d')
#      ax1.set_xlim(left=mpl_dates.date2num(start_assim)-1,right=mpl_dates.date2num(final_assim)+1)
#      ax1.plot(fds, np.zeros_like(fds),'k--')
#      ax1.grid()
#      if (i_diag == 0):
#         ax1.set_ylim(bottom = min(0,np.min(diags[i_diag,0,i_var,:].squeeze())), top = 1.6*np.max(diags[i_diag,0,i_var,:].squeeze()))
#         # Add number of observations assimilated
#         ax2 = ax1.twinx()
#         ax2.plot(fds, np.sum(N_QC[i_var,:,:],axis=0), 'o', markerfacecolor='w',markeredgecolor='b')
#         ax2.plot(fds, N_QC[i_var,0,:].squeeze(), 'b+')
#         ax2.set_ylim(bottom = -500, top = 1.1*np.max(np.sum(N_QC[i_var,:,:],axis=0)))
#         ax2.set_ylabel('# of obs : o=possible, +=assimilated', color='b')
#         ax2.set_xlim(left=mpl_dates.date2num(start_assim)-1,right=mpl_dates.date2num(final_assim)+1)
#         for tl in ax2.get_yticklabels():
#            tl.set_color('b')
#         # Put legend on graph
#         h1, l1 = ax1.get_legend_handles_labels()
#         ax2.legend(h1,l1,fancybox=True)
#   figname=dir_pictures + '/Diags_rt_assim_' + simu + '_' + variname[i_var] + '.png'
#   plt.tight_layout()
#   plt.savefig(figname)
#   print(figname)

plt.close('all')

QC_legend = ['assimilated','evaluated','assimilated, posterior failed','evaluated, posterior failed','excluded (outside domain)','excluded (namelist)','excluded (prior QC)','excluded (outlier)']

index = np.arange(n_time) + 0.3
bar_width = 0.6
#colors = rt_colormaps['paldif20'](np.linspace(0.1, 1, n_qc))
colors = rt_colormaps['eke2'](np.linspace(0.1, 1, n_qc))

fig = plt.figure(figsize=[15.,10.]);plt.clf()
for i_var in xrange(0,n_var):
	ax1 = fig.add_subplot(1,3,i_var+1)
	y_offset = np.array([0.0] * n_time)
	for i_QC in range(n_qc):
		ax1.bar(fds, N_QC[i_var,i_QC,:], bar_width, bottom=y_offset, color=colors[i_QC],label=QC_legend[i_QC],edgecolor='none')
		y_offset = y_offset + N_QC[i_var,i_QC,:]
        rt_plotbox.xaxis_date(fds,ax=ax1,step=date_step,date_format='%m/%d')
        if i_var == 0:
	   ax1.legend(loc=4)
	plt.title(variname[i_var])
#        if i_var>0:
        ax1.set_ylim(bottom = 0, top = 14000)
        ax1.set_xlim(left=mpl_dates.date2num(start_assim)-1,right=mpl_dates.date2num(final_assim)+1)
plt.tight_layout()
figname=dir_pictures + '/Diags_obs_N_' + simu + '.png'
plt.savefig(figname)
print(figname)








