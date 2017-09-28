# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 15:06:01 2016

@author: romain
"""

print('----------------------------------------------------------------')
print('                        Post-processing Obs Dart                ')
print('----------------------------------------------------------------')

#%% Toolboxes

from param_dart import *
import rt_netcdf_tools
import collections


#%% Diagnosis
rank_hist = np.zeros((3,N_days,N_members+1))
rank_hist_good = np.zeros((3,N_days,N_members+1))
rank_bins = np.arange(-0.5,31.5,1)

file_list=[]
for i_cur,dday in enumerate(datevec_assim):
    print "Day " + dday.strftime('%Y/%m/%d') + " of " + final_assim.strftime('%Y/%m/%d')
    # Get data
    file_obs = glob.glob(dir_obs+'obs_seq.*.final.'+dday.strftime('%Y%m%d')+'.nc')[0];
    file_list.append(file_obs)
    nc_obs = ncdf.Dataset(file_obs,'r')
    obs_val   = nc_obs.variables['observations'][:,0]
    obs_type  = nc_obs.variables['obs_type'][:]
    obs_qc    = nc_obs.variables['qc'][:,1]
    obs_rank  = nc_obs.variables['obs_rank'][:]
    nc_obs.close()
    N_obs = len(obs_val)
    
    # Indices of obs types
    var_type=['SATELLITE_SST','T_PROFILES','S_PROFILES']
    idx_domain = obs_qc!=4
    idx = np.ones((3,len(obs_type)), dtype=bool)
    idx[0,:] = np.logical_and(obs_type==52,idx_domain)
    idx[1,:] = np.logical_and(obs_type==16,idx_domain)
    idx[2,:] = np.logical_and(obs_type==15,idx_domain)
    
    # Indices of good data
    idx_OK   = obs_qc<4
    idx_badS = np.logical_and(obs_val<20,obs_type==15)

    for i_type in xrange(3):
        idx_tmp=np.logical_and(idx[i_type],~idx_badS)
        rank_hist[i_type,i_cur,:],bins = np.histogram(obs_rank[idx_tmp],bins=rank_bins)
        idx_tmp_good=np.logical_and(idx_tmp,idx_OK)
        rank_hist_good[i_type,i_cur,:],bins = np.histogram(obs_rank[idx_tmp_good],bins=rank_bins)

time=[(dday - dtime.datetime(1900,1,1)).days for dday in datevec_assim]

#########################################################################################
# NetCDF file
#########################################################################################

# NetCDF parameters
dimensions =  collections.OrderedDict([\
   ('time',N_days),\
   ('vartype',3),\
   ('QC_val',8),\
   ('rank_bins',N_members+1)])
attributes = collections.OrderedDict([\
   ('author','Romain Escudier'),\
   ('creation_date',dtime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),\
   ('list_obs_files',"\n".join(file_list)),\
   ('Variable_type',[i+',' for i in var_type])])
# Prepare netCDF
nc_file = rt_netcdf_tools.nc_object(attributes,dimensions)
# Add variables
time_att=collections.OrderedDict([('units','days since 1900-1-1'),('calendar','Gregorian')])
nc_file.add_variable('time',time,vardim=('time'),varatt=time_att)
nc_file.add_variable('rank_bins',np.arange(31),vardim=('rank_bins'),varatt={'long_name':'Bins of rank histogram'})
nc_file.add_variable('Rank_hist',rank_hist,vardim=('vartype','time','rank_bins'),varatt={'long_name':'Rank histogram'})
nc_file.add_variable('Rank_hist_good',rank_hist_good,vardim=('vartype','time','rank_bins'),varatt={'long_name':'Rank histogram for non outliers'})

# Create file
nc_file.create_file(dir_obs+'obs_diag_rankhist.nc')

#file_obs_diag = dir_obs_diag+'obs_diag_rankhist.nc'
#nc_diags = ncdf.Dataset(file_obs_diag,'r')
#rank_hist=nc_diags.variables['Rank_hist'][:]






#from mpl_toolkits.mplot3d import Axes3D
#
#col_names = ['taupe','rust','olive','teal','hyperblue','aubergine','burgundy']
#
## Coordinates
#xpos,ypos = np.meshgrid(np.arange(N_days), np.arange(31))
#xpos = xpos
#ypos = ypos
#zpos = np.zeros_like(xpos)
## Bars
#dx = 0.9 * np.ones_like(zpos)
#dy = dx.copy()
#dz = rank_hist[0,:,:].transpose()
#
#fig = plt.figure(figsize=[25.,15.])
#ax = fig.add_subplot(111, projection='3d')
#for i_day in xrange(N_days):
#    bh = ax.bar3d(xpos[:,i_day], ypos[:,i_day], zpos[:,i_day], dx[:,i_day], dy[:,i_day], dz[:,i_day], color=rt_colors[col_names[np.mod(i_day,7)]], zsort='average')
#    bh.set_edgecolor('none')
#ax.view_init(elev=30,azim=-20)
#figname=dir_pictures + '/Rank_hist_py_' + simu + '_SST.png'
#plt.savefig(figname)
#print(figname)





#x, y = np.random.rand(2, 100) * 4
#hist, xedges, yedges = np.histogram2d(x, y, bins=4, range=[[0, 4], [0, 4]])
#
## Construct arrays for the anchor positions of the 16 bars.
## Note: np.meshgrid gives arrays in (ny, nx) so we use 'F' to flatten xpos,
## ypos in column-major order. For numpy >= 1.7, we could instead call meshgrid
## with indexing='ij'.
#xpos, ypos = np.meshgrid(xedges[:-1] + 0.25, yedges[:-1] + 0.25)
#xpos = xpos.flatten('F')
#ypos = ypos.flatten('F')
#zpos = np.zeros_like(xpos)
#
## Construct arrays with the dimensions for the 16 bars.
#dx = 0.5 * np.ones_like(zpos)
#dy = dx.copy()
#dz = hist.flatten()
#
#ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='b', zsort='average')
#
#plt.close('all')








