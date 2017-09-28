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
N_copy = len(copy)
N_vari = len(sel_type)
N_layer = len(layer)
var_type = [var_type[i] for i in sel_type]
var_id   = [var_id[i] for i in sel_type]



rmse_good = np.ma.ones((N_copy,N_vari,N_layer,N_days))*-9999
bias_good = np.ma.ones((N_copy,N_vari,N_layer,N_days))*-9999
spre_good = np.ma.ones((N_copy,N_vari,N_layer,N_days))*-9999
totspre_good = np.ma.ones((N_copy,N_vari,N_layer,N_days))*-9999

rmse = np.ma.ones((N_copy,N_vari,N_layer,N_days))*-9999
bias = np.ma.ones((N_copy,N_vari,N_layer,N_days))*-9999
spre = np.ma.ones((N_copy,N_vari,N_layer,N_days))*-9999
totspre = np.ma.ones((N_copy,N_vari,N_layer,N_days))*-9999

N_QC = np.zeros((N_vari,N_layer,8,N_days))

file_list=[]
for i_cur,dday in enumerate(datevec_assim):
    print "Day " + dday.strftime('%Y/%m/%d') + " of " + final_assim.strftime('%Y/%m/%d')
    # Get data
    file_obs = glob.glob(dir_obs+'obs_seq.*.final.'+dday.strftime('%Y%m%d')+'.nc')[0];
    file_list.append(file_obs)
    nc_obs = ncdf.Dataset(file_obs,'r')
    obs_lon   = nc_obs.variables['location'][:,0]
    obs_lat   = nc_obs.variables['location'][:,1]
    obs_dep   = nc_obs.variables['location'][:,2]
    obs_val   = nc_obs.variables['observations'][:,0]
    obs_prio  = nc_obs.variables['observations'][:,1]
    obs_post  = nc_obs.variables['observations'][:,2]
    obs_sprp  = nc_obs.variables['observations'][:,3]
    obs_spra  = nc_obs.variables['observations'][:,4]
    obs_errv  = nc_obs.variables['observations'][:,-1]
    obs_qc    = nc_obs.variables['qc'][:,1]
    obs_type  = nc_obs.variables['obs_type'][:]
    nc_obs.close()
    N_obs = len(obs_val)
    
    # Indices of obs types
    idx = np.zeros((N_vari,len(obs_type)), dtype=bool)
    for i_type in xrange(N_vari):
       if isinstance(var_id[i_type],list):
          for id_type_sensor in var_id[i_type]:
             idx[i_type,:] = (idx[i_type,:]) | (obs_type==id_type_sensor)
       else:
          idx[i_type,:] = (obs_type==var_id[i_type])
    
    # Indices of good data
    idx_OK   = obs_qc==0
    idx_badS = np.logical_and(obs_val<20,obs_type==15)

    # Squared error
    se = np.ma.empty((2,N_obs)) 
    se[0,:] = (obs_val-obs_prio)**2 # Prior
    se[1,:] = (obs_val-obs_post)**2 # Analysis

    # Bias
    bias_obs = np.ma.empty((2,N_obs))
    bias_obs[0,:] = obs_prio-obs_val
    bias_obs[1,:] = obs_post-obs_val

    # Spread
    spre_obs = np.ma.empty((2,N_obs))
    spre_obs[0,:] = obs_sprp
    spre_obs[1,:] = obs_spra
    spre_obs_tot = np.ma.empty((2,N_obs))
    spre_obs_tot[0,:] = np.sqrt(obs_sprp**2+obs_errv)
    spre_obs_tot[1,:] = np.sqrt(obs_spra**2+obs_errv)

    for i_layer in xrange(N_layer):
        idx_layer=(obs_dep>=layer[i_layer][0] ) & (obs_dep<layer[i_layer][1]) & ~idx_badS
        for i_type in xrange(N_vari):
            idx_tmp=np.logical_and(idx[i_type],idx_layer)
            idx_tmp_good=np.logical_and(idx_tmp,idx_OK)
            
            if idx_tmp_good.sum()>0:
               # Number of assimilated/rejected/... observations
               for i_qc in xrange(8):
                   idx_QC = (obs_qc == i_qc)
                   N_QC[i_type,i_layer,i_qc,i_cur] = np.sum(np.logical_and(idx_QC,idx_tmp))
               
               # Diagnostics
               for i_copy in xrange(N_copy):
                  # Time series
                  rmse[i_copy,i_type,i_layer,i_cur]         = np.sqrt(np.mean(se[i_copy,idx_tmp]))
                  bias[i_copy,i_type,i_layer,i_cur]         = np.mean(bias_obs[i_copy,idx_tmp])
                  spre[i_copy,i_type,i_layer,i_cur]         = np.mean(spre_obs[i_copy,idx_tmp])
                  totspre[i_copy,i_type,i_layer,i_cur]      = np.mean(spre_obs_tot[i_copy,idx_tmp])
                  rmse_good[i_copy,i_type,i_layer,i_cur]    = np.sqrt(np.mean(se[i_copy,idx_tmp_good]))
                  bias_good[i_copy,i_type,i_layer,i_cur]    = np.mean(bias_obs[i_copy,idx_tmp_good])
                  spre_good[i_copy,i_type,i_layer,i_cur]    = np.mean(spre_obs[i_copy,idx_tmp_good])
                  totspre_good[i_copy,i_type,i_layer,i_cur] = np.mean(spre_obs_tot[i_copy,idx_tmp_good])
              
rmse_good = np.ma.masked_where(rmse_good==-9999,rmse_good)
bias_good = np.ma.masked_where(bias_good==-9999,bias_good)
spre_good = np.ma.masked_where(spre_good==-9999,spre_good)
totspre_good = np.ma.masked_where(totspre_good==-9999,totspre_good)

rmse = np.ma.masked_where(rmse==-9999,rmse)
bias = np.ma.masked_where(bias==-9999,bias)
spre = np.ma.masked_where(spre==-9999,spre)
totspre = np.ma.masked_where(totspre==-9999,totspre)

time=[(dday - dtime.datetime(1900,1,1)).days for dday in datevec_assim]


#########################################################################################
# NetCDF file
#########################################################################################

# NetCDF parameters
dimensions =  collections.OrderedDict([('time',N_days), ('copy',N_copy),('vartype',N_vari),\
   ('layer',N_layer),('QC_val',8)])
   #,('lon_cell',len(lon_cell)-1),('lat_cell',len(lat_cell)-1)])
attributes = collections.OrderedDict([('author','Romain Escudier'),\
   ('creation_date',dtime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),\
   ('Variable_type',[i+',' for i in var_type]),\
   ('Copy',[i+',' for i in copy]),\
   ('Layer',str(layer)),\
   ('list_obs_files',"\n".join(file_list))])
# Prepare netCDF
nc_file = rt_netcdf_tools.nc_object(attributes,dimensions)
# Prepare variables
time_att=collections.OrderedDict([('units','days since 1900-1-1'),('calendar','Gregorian')])
rmse_att=collections.OrderedDict([('long_name','RMSE at observation points'),('_FillValue',-9999.)])
bias_att=collections.OrderedDict([('long_name','Bias at observation points'),('_FillValue',-9999.)])
spre_att=collections.OrderedDict([('long_name','Spread at observation points'),('_FillValue',-9999.)])
totspre_att=collections.OrderedDict([('long_name','Total spread (observation error added) at observation points'),('_FillValue',-9999.)])
qc_att=collections.OrderedDict([('long_name','Number of observation for each QC value')])
# Add variables
nc_file.add_variable('time'            ,time        ,vardim=('time'),varatt=time_att)
nc_file.add_variable('RMSE'            ,rmse        ,vardim=('copy','vartype','layer','time'),varatt=rmse_att)
nc_file.add_variable('RMSE_good'       ,rmse_good   ,vardim=('copy','vartype','layer','time'),varatt=rmse_att)
nc_file.add_variable('Bias'            ,bias        ,vardim=('copy','vartype','layer','time'),varatt=bias_att)
nc_file.add_variable('Bias_good'       ,bias_good   ,vardim=('copy','vartype','layer','time'),varatt=bias_att)
nc_file.add_variable('Spread'          ,spre        ,vardim=('copy','vartype','layer','time'),varatt=spre_att)
nc_file.add_variable('Spread_good'     ,spre_good   ,vardim=('copy','vartype','layer','time'),varatt=spre_att)
nc_file.add_variable('TotalSpread'     ,totspre     ,vardim=('copy','vartype','layer','time'),varatt=totspre_att)
nc_file.add_variable('TotalSpread_good',totspre_good,vardim=('copy','vartype','layer','time'),varatt=totspre_att)
nc_file.add_variable('N_obs_QC'        ,N_QC        ,vardim=('vartype','layer','QC_val','time'),varatt=qc_att)

# Create file
nc_file.create_file(dir_obs+'obs_diag_romain.nc')

