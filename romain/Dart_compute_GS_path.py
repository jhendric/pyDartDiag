
print('----------------------------------------------------------------')
print('                        Post-processing Obs Dart                ')
print('----------------------------------------------------------------')

#%% Toolboxes

from param_dart import *
import rt_netcdf_tools
import rt_stats_tools
import collections
import sys

mydepth=200

#########################################################################################
#%% Parameters
#########################################################################################
dir_hindc = ['/Volumes/P10/ROMS/NWA/','/Volumes/P10/ROMS/NWA/','/Volumes/P8/ROMS/NWA/']
simus_hindc = ['NWA-RD.HCSODA3R','NWA-RD.HCSODA3DFS5','NWA-RD.HCSODA3JRA55']
N_hindc = len(simus_hindc)

#########################################################################################
#%% Coefficient for 200m slice
#########################################################################################

z = RomsGrid.grid.variables['z_r'].value
N_levels = z.shape[0]
# Get ocean points
idx_ocean = RomsGrid.grid.variables['mask_rho'].value==1
N_ocean = idx_ocean.sum()
# Pad the depths
z_o = np.zeros((z.shape[0]+2,N_ocean))
z_o[0,:] = -np.infty
z_o[1:-1,:] = z[:,idx_ocean]
z_o = np.flipud(z_o)
# Find upper level for interpolation
zo200  = np.abs(z_o)>200
idx_up = np.logical_xor(zo200[:-1,:],zo200[1:,:])
lev_up = np.dot(np.arange(N_levels+1),(0+idx_up))
lev_dn = lev_up+1
id_up = np.ravel_multi_index(np.array([lev_up,np.arange(N_ocean)]),z_o.shape)
id_dn = np.ravel_multi_index(np.array([lev_dn,np.arange(N_ocean)]),z_o.shape)
# Compute interpolation weights between the data values
z_o_ravel = z_o.ravel()
dist_up=abs(abs(z_o_ravel[id_up])-mydepth);
dist_dn=abs(abs(z_o_ravel[id_dn])-mydepth);
alpha = dist_dn/(dist_up+dist_dn);


lon_rho = RomsGrid.grid.variables['lon_rho'].value-360
lat_rho = RomsGrid.grid.variables['lat_rho'].value

#########################################################################################
#%% Diagnosis
#########################################################################################

N_interp=1000
for dday in datevec_simu_month:
   print "Month : " + dday.strftime('%Y/%m')
   GS_paths_T=[]
   GS_paths_Z=[]
   ncfile = dir_obs+'GS_paths_'+dday.strftime('%Y%m')+'.nc'
   if not os.path.isfile(ncfile):
      # Ensemble assimilation
      for member in xrange(N_members):
         print " - member " + "%03d"%(member+1)
         # Get data
         file_avg = dir_average + '/m' + "%03d"%(member+1) + '/' + simu + '_avg_monthly_' + dday.strftime('%Y%m') + '.nc'
         nc_avg = ncdf.Dataset(file_avg,'r')
         zeta = nc_avg['zeta'][:,:,:].squeeze()
         temp = nc_avg['temp'][0,:,:,:]
         nc_avg.close()
     
         # Get 200m slice
         temp_tmp = np.empty((z.shape[0]+2,N_ocean))
         temp_tmp[0,:] = np.nan
         temp_tmp[1:-1,:] = temp[:,idx_ocean]
         temp_tmp[-1,:] = temp_tmp[-2,:]
         temp_tmp = np.flipud(temp_tmp).ravel()
         
         temp_tmp_200m = temp_tmp[id_up]*alpha+temp_tmp[id_dn]*(1.-alpha)
         temp_200m = np.ones(temp.shape[1:])*np.nan
         temp_200m[idx_ocean] = temp_tmp_200m


         temp_200m[:,0:250]=np.nan
         zeta[:,0:250]=np.nan
     
         # Find the 15degC limit
         cont_t = plt.contour(lon_rho,lat_rho,temp_200m,[15])
         cont_z = plt.contour(lon_rho,lat_rho,zeta,[-.30])
         plt.close() # contour triggers a figure
         cont_t = rt_dart_tools.get_continuous_contours(cont_t.allsegs[0])
         cont_z = rt_dart_tools.get_continuous_contours(cont_z.allsegs[0])
         N_max=0
         for icont in cont_t:
            if len(icont)>N_max:
               max_cont_t = icont
               N_max = len(icont)
         max_cont_t=max_cont_t[::-1,:]
         GS_paths_T.append(max_cont_t)
         N_max=0
         for icont in cont_z:
            if len(icont)>N_max:
               max_cont_z = icont
               N_max = len(icont)
         max_cont_z=max_cont_z[::-1,:]
         GS_paths_Z.append(max_cont_z)

#########################################################################################
#%% Reinterpolation
#########################################################################################
      GS_paths_mat = np.empty((2,len(GS_paths_T),N_interp,2))
      GS_paths_mean= np.empty((2,N_interp,2))
      GS_paths_std_coord = np.empty((2,N_interp,2))
      s_vec = np.linspace(0,1,N_interp)
      for icur,cont_tmp in enumerate(GS_paths_T):
         s_vec_tmp = rt_stats_tools.gc_dist_diff(cont_tmp[:,0],cont_tmp[:,1])
         s_vec_tmp = np.append(0,np.cumsum(s_vec_tmp/(s_vec_tmp.sum())))
         GS_paths_mat[0,icur,:,0] = np.interp(s_vec,s_vec_tmp,cont_tmp[:,0])
         GS_paths_mat[0,icur,:,1] = np.interp(s_vec,s_vec_tmp,cont_tmp[:,1])
      for icur,cont_tmp in enumerate(GS_paths_Z):
         s_vec_tmp = rt_stats_tools.gc_dist_diff(cont_tmp[:,0],cont_tmp[:,1])
         s_vec_tmp = np.append(0,np.cumsum(s_vec_tmp/(s_vec_tmp.sum())))
         GS_paths_mat[1,icur,:,0] = np.interp(s_vec,s_vec_tmp,cont_tmp[:,0])
         GS_paths_mat[1,icur,:,1] = np.interp(s_vec,s_vec_tmp,cont_tmp[:,1])
      for ivar in xrange(2):
         GS_paths_mean[ivar,:,0] = GS_paths_mat[ivar,0:N_members,:,0].mean(axis=0)
         GS_paths_mean[ivar,:,1] = GS_paths_mat[ivar,0:N_members,:,1].mean(axis=0)
         dist_tmp = np.empty((N_members,N_interp))
         for icur in xrange(N_members):
            dist_tmp[icur,:] = np.sqrt(((GS_paths_mat[ivar,icur,:,0]-GS_paths_mean[ivar,:,0])\
                                      *np.cos((np.pi/180)*GS_paths_mean[ivar,:,1]))**2\
                                      +(GS_paths_mat[ivar,icur,:,1]-GS_paths_mean[ivar,:,1])**2)
         GS_paths_std = dist_tmp.std(axis=0)
         ang_pent=np.arctan2(np.diff(GS_paths_mean[ivar,:,1]),np.diff(GS_paths_mean[ivar,:,0]))
         ang_pent=np.append(ang_pent[0],ang_pent)
         GS_paths_std_coord[ivar,:,0] = -GS_paths_std*np.sin(ang_pent)
         GS_paths_std_coord[ivar,:,1] =  GS_paths_std*np.cos(ang_pent)


#########################################################################################
# NetCDF file
#########################################################################################

      time_std=(dday-dtime.datetime(1900, 1, 1, 0, 0)).days

      # NetCDF parameters
      dimensions =  collections.OrderedDict([('time',None),\
                                             ('variable',2),\
                                             ('members',N_members),\
                                             ('along_coord',N_interp),\
                                             ('coordinates',2)])
      attributes = collections.OrderedDict([('long_name','Paths of Gulf Stream from contours of T200 (15degC, variable 1) and zeta (0.2m, variable 2)'),\
         ('author','Romain Escudier'),\
         ('simu',simu),\
         ('creation_date',dtime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),\
         ('date',dday.strftime('%Y%m'))])
      # Prepare netCDF
      nc_file = rt_netcdf_tools.nc_object(attributes,dimensions)
      # Prepare variables
      time_att      = collections.OrderedDict([('units','days since 1900-1-1'),('calendar','Gregorian')])
      path_att      = collections.OrderedDict([('long_name','GS paths coordinates'),('_FillValue',-9999.)])
      path_mean_att = collections.OrderedDict([('long_name','Mean GS paths coordinates'),('_FillValue',-9999.)])
      path_stdc_att  = collections.OrderedDict([('long_name','Coords of std GS paths coordinates'),('_FillValue',-9999.)])
      # Add variables
      nc_file.add_variable('time'            ,time_std           ,vardim=('time',),varatt=time_att)
      nc_file.add_variable('GS_paths'        ,np.expand_dims(GS_paths_mat,axis=0),\
                vardim=('time','variable','members','along_coord','coordinates'),varatt=path_att)
      nc_file.add_variable('GS_paths_mean'   ,np.expand_dims(GS_paths_mean,axis=0),\
                vardim=('time','variable','along_coord','coordinates'),varatt=path_mean_att)
      nc_file.add_variable('GS_paths_stdc'   ,np.expand_dims(GS_paths_std_coord,axis=0),\
                vardim=('time','variable','along_coord','coordinates'),varatt=path_stdc_att)
      
      # Create file
      nc_file.create_file(ncfile)


sys.exit(0)




#
#
fig = plt.figure(figsize=[20.,20.])
m=rt_plotbox.rt_plot_2D(np.array([]),np.array([]),np.array([]),fontsiz=14,plotitle='GS path')
plt.plot(max_cont[:,0],max_cont[:,1])
i_curp=[]
for i_cur,i_seg in enumerate(cont_all):
   p.append(plt.plot(i_seg[:,0],i_seg[:,1],label=str(i_cur)))
plt.legend()
plt.plot(pos1[:,0],pos1[:,1],'*')
plt.plot(pos2[:,0],pos2[:,1],'o')

#fig = plt.figure(figsize=[20.,20.])
#m=rt_plotbox.rt_plot_2D(np.array([]),np.array([]),np.array([]),fontsiz=14,plotitle='GS path')
#plt.pcolor(lon_rho,lat_rho,temp_200m,vmin=0,vmax=25)
#
#
#
#
fig = plt.figure(figsize=[20.,20.])
m=rt_plotbox.rt_plot_2D(np.array([]),np.array([]),np.array([]),fontsiz=14,geo=[-85,-48,25,45],\
        stepX=5.,stepY=5)
p=[]
for i_cur,i_seg in enumerate(GS_paths_T):
   p.append(plt.plot(i_seg[:,0],i_seg[:,1],label='member '+"%03d"%(i_cur+1)))
   plt.plot(i_seg[-1,0],i_seg[-1,1],'o')
plt.legend()

for i_cur,i_seg in enumerate(GS_paths_T):
   p.append(plt.plot(i_seg[:,0],i_seg[:,1],'k',label='member '+"%03d"%(i_cur+1)))
for i_cur,i_seg in enumerate(GS_paths_Z):
   p.append(plt.plot(i_seg[:,0],i_seg[:,1],'r',label='member '+"%03d"%(i_cur+1)))




fig = plt.figure(figsize=[20.,20.])
m=rt_plotbox.rt_plot_2D(np.array([]),np.array([]),np.array([]),fontsiz=14,geo=[-85,-48,25,45],\
        stepX=5.,stepY=5)
p=[]
for i_cur,i_seg in enumerate(GS_paths_T):
   p.append(plt.plot(i_seg[:,0],i_seg[:,1],'k',label='member '+"%03d"%(i_cur+1)))
for i_cur,i_seg in enumerate(GS_paths_Z):
   p.append(plt.plot(i_seg[:,0],i_seg[:,1],'r',label='member '+"%03d"%(i_cur+1)))



