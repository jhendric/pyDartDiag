
print('----------------------------------------------------------------')
print('                        Post-processing Obs Dart                ')
print('----------------------------------------------------------------')

#%% Toolboxes

import numpy as np
import netCDF4 as ncdf
import datetime as dtime
import matplotlib.pylab as plt
import matplotlib.cm as cm
import collections
import glob
import sys
import os
import rt_netcdf_tools
import rt_stats_tools


#########################################################################################
#%% Parameters
#########################################################################################
dir_aviso = '/Volumes/P8/DART/AVISO/msla/ftp.sltac.cls.fr/Core/SEALEVEL_GLO_PHY_L4_REP_OBSERVATIONS_008_047/dataset-duacs-rep-global-merged-allsat-phy-l4-v3/monthly/'
pref_aviso= 'dt_global_allsat_phy_l4_'
my_year = 2011

#########################################################################################
#%% Get grid parameters
#########################################################################################

file_aviso = dir_aviso + str(my_year) + '/' + pref_aviso + str(my_year) + '01_monthly.nc'
nc_aviso = ncdf.Dataset(file_aviso,'r')
lat_aviso = nc_aviso['latitude'][:]
lon_aviso = nc_aviso['longitude'][:]-360
nc_aviso.close()

ilatmin = np.argwhere(lat_aviso>25)[0][0]
ilatmax = np.argwhere(lat_aviso<50)[-1][0]
ilonmin = np.argwhere(lon_aviso>-85)[0][0]
ilonmax = np.argwhere(lon_aviso<-45)[-1][0]

lat_aviso = lat_aviso[ilatmin:ilatmax]
lon_aviso = lon_aviso[ilonmin:ilonmax]

#########################################################################################
#%% Diagnosis
#########################################################################################


print "Computing GS path for year " + str(my_year)
for imonth in xrange(12):
   dday = dtime.datetime(my_year,imonth+1,1)
   print "Month : " + dday.strftime('%Y/%m')
   ncfile = dir_aviso+'GS_paths_'+dday.strftime('%Y%m')+'.nc'
   if not os.path.isfile(ncfile):
      # Get data
      file_aviso = dir_aviso + str(my_year) + '/' + pref_aviso + dday.strftime('%Y%m') + '_monthly.nc'
      nc_aviso = ncdf.Dataset(file_aviso,'r')
      adt = nc_aviso['adt'][:,ilatmin:ilatmax,ilonmin:ilonmax].squeeze()
      nc_aviso.close()
   
      # Find the 25cm limit
      cont = plt.contour(lon_aviso,lat_aviso,adt,[0.25])
      plt.close() # contour triggers a figure
      pos1=np.empty((len(cont.allsegs[0]),2))
      pos2=np.empty((len(cont.allsegs[0]),2))
      cont_all=[]
      for icur,icont in enumerate(cont.allsegs[0]):
         pos1[icur,:] = icont[0,:]
         pos2[icur,:] = icont[-1,:]
         cont_all.append(icont)
      id_cont=np.arange(len(cont_all))
      icur = 0
      N_cont=len(cont_all)
      while (icur < N_cont):
         if any(id_cont==icur):
            icur_cont = np.argwhere(id_cont==icur).squeeze()
            dist = [rt_stats_tools.gc_dist(pos1[icur_cont,0],pos1[icur_cont,1],pos2[i,0],pos2[i,1]) for i in xrange(len(cont_all))]
            dist[icur_cont]=1000000
            imindist=np.argmin(dist)
            mindist=dist[imindist]
            #print icur, icur_cont, imindist, mindist
            if (mindist<50000):
               cont_all[icur_cont]=np.concatenate((cont_all[imindist],cont_all[icur_cont]))
               cont_all.pop(imindist)
               idx_new=(id_cont!=id_cont[imindist])
               pos2 = pos2[idx_new,:]
               pos1[icur_cont,:]=pos1[imindist,:]
               pos1 = pos1[idx_new,:]
               id_cont = id_cont[idx_new]
               icur=icur-1
         icur=icur+1
      N_max=0
      for icont in cont_all:
         if len(icont)>N_max:
            max_cont = icont
            N_max = len(icont)
            max_cont=max_cont[::-1,:]
      GS_path = max_cont
   
#########################################################################################
#%% Reinterpolation
#########################################################################################
      N_interp=1000
      GS_path_mat = np.empty((N_interp,2))
      s_vec = np.linspace(0,1,N_interp)
      s_vec_tmp = rt_stats_tools.gc_dist_diff(GS_path[:,0],GS_path[:,1])
      s_vec_tmp = np.append(0,np.cumsum(s_vec_tmp/(s_vec_tmp.sum())))
      GS_path_mat[:,0] = np.interp(s_vec,s_vec_tmp,GS_path[:,0])
      GS_path_mat[:,1] = np.interp(s_vec,s_vec_tmp,GS_path[:,1])
   
#########################################################################################
# NetCDF file
#########################################################################################
   
      time_std=(dday-dtime.datetime(1900, 1, 1, 0, 0)).days
      
      # NetCDF parameters
      dimensions =  collections.OrderedDict([('time',None),\
                                             ('along_coord',N_interp),\
                                             ('coordinates',2)])
      attributes = collections.OrderedDict([('long_name','Paths of Gulf Stream for AVISO'),\
         ('author','Romain Escudier'),\
         ('creation_date',dtime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),\
         ('date',dday.strftime('%Y%m'))])
      # Prepare netCDF
      nc_file = rt_netcdf_tools.nc_object(attributes,dimensions)
      # Prepare variables
      time_att      = collections.OrderedDict([('units','days since 1900-1-1'),('calendar','Gregorian')])
      path_att      = collections.OrderedDict([('long_name','GS paths coordinates'),('_FillValue',-9999.)])
      # Add variables
      nc_file.add_variable('time'    ,np.expand_dims(time_std,axis=0)   ,vardim=('time',),varatt=time_att)
      nc_file.add_variable('GS_paths',np.expand_dims(GS_path_mat,axis=0),vardim=('time','along_coord','coordinates'),varatt=path_att)
      
      # Create file
      nc_file.create_file(ncfile)


sys.exit(0)



