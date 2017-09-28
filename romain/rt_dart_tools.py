# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 11:08:37 2016

@author: romain
"""

import numpy as np
import rt_netcdf_tools
import collections
import datetime as dtime
import rt_stats_tools


def dart_spread(model_state):
    n,m = model_state.shape
    mean_state = np.mean(model_state,0)
    diff_state = model_state-(np.tile(mean_state,(n,1)))
    spread=_rms(diff_state,0);
    return spread

    
def _rms(X,dim):
    siz = np.shape(X)
    my_rms=np.sqrt(np.sum(np.square(X),axis=dim))/np.sqrt(siz[dim]-1)
    return my_rms


def calc_cell_prctile(lon,lat,val,lon_cell,lat_cell,perc):
    Nlat = len(lat_cell)
    Nlon = len(lon_cell)
    perc_cell = np.empty((Nlat-1,Nlon-1))
    perc_cell[:] = np.nan

    for longi in xrange(Nlon-1):
        for lati in xrange(Nlat-1):
            idx = np.logical_and.reduce((lon>=lon_cell[longi],lon<lon_cell[longi+1],lat>=lat_cell[lati],lat<lat_cell[lati+1]))
            if idx.sum()>0:
                perc_cell[lati,longi] = np.percentile(val[idx],perc)

    return perc_cell


def calc_cell_sum_N(lon,lat,val,lon_cell,lat_cell):
    Nlat = len(lat_cell)
    Nlon = len(lon_cell)
    nb_cell = np.zeros((Nlat-1,Nlon-1))
    sum_cell = np.zeros((Nlat-1,Nlon-1))

    for longi in xrange(Nlon-1):
        for lati in xrange(Nlat-1):
            idx = np.logical_and.reduce((lon>=lon_cell[longi],lon<lon_cell[longi+1],lat>=lat_cell[lati],lat<lat_cell[lati+1],val.mask==False))
            N=idx.sum()
            if N>0:
                nb_cell[lati,longi] = N
                sum_cell[lati,longi] = val[idx].sum()

    return sum_cell,nb_cell

def get_continuous_contours(cont_tmp):
   pos1=np.empty((len(cont_tmp),2))
   pos2=np.empty((len(cont_tmp),2))
   cont_all=[]
   for icur,icont in enumerate(cont_tmp):
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
   return cont_all



def read_dart_obs_analysis(file_obs):
   # Open file
   fid = open(file_obs,'r')
 
   # Get header
   header = _read_dart_1obs_list(fid)
   
   # Get key parameters
   string = header[-2].split()
   start_obs = int(string[1])
   final_obs = int(string[3])
   N_obs = final_obs-start_obs+1
   string = next((s for s in header if 'num_obs' in s), None)
   N_obs = int(string.split()[1])
   string = next((s for s in header if 'num_copies' in s), None)
   N_copies = int(string.split()[1])
   N_qc = int(string.split()[3])
   if (N_qc > 1):
      is_post = True
      N_members = (N_copies-5)/2
   else:
      is_post = False
   N_obstype = int(header[2].split()[0])
   
   CopyMetaData     = [el.strip()+'\n' for el in header[5+N_obstype:N_copies+5+N_obstype]]
   CopyMetaData.append('observation error variance')
   QCMetaData       = [el.strip()+';' for el in header[N_copies+N_obstype+5:N_copies+N_obstype+5+N_qc]]
   ObsTypesMetaData = [el.strip()+';' for el in header[3:3+N_obstype]]

   # Initialize
   obs      = np.ma.empty((N_obs,N_copies+1))
   time     = np.empty((N_obs))
   obs_type = np.empty((N_obs))
   qc       = np.empty((N_obs,N_qc))
   loc      = np.empty((N_obs,3))
   vert     = np.empty((N_obs))
   if is_post:
      obs_rank = np.zeros(N_obs)

   # Read observations
   for i_obs in xrange(N_obs):
      obs_list = _read_dart_1obs_list(fid)
      # Observations and members
      obs[i_obs,0:N_copies] = [float(val.split()[0]) for val in obs_list[0:N_copies]]
      # Error variance
      obs[i_obs,N_copies]   = float(obs_list[N_copies+7+N_qc].split()[0])
      # Quality control
      qc[i_obs,:]           = [float(val.split()[0]) for val in obs_list[N_copies:N_copies+N_qc]]
      # Type of observation
      obs_type[i_obs]       = int(obs_list[N_copies+5+N_qc].split()[0])
      # Dart links
      links                 = [int(val) for val in obs_list[N_copies+N_qc].split()]
      # Coordinates
      loc_tmp               = [float(val) for val in obs_list[N_copies+3+N_qc].split()]
      loc[i_obs,:]          = loc_tmp[0:3]
      vert[i_obs]           = loc_tmp[3]
      # Time
      time_tmp              = [int(val) for val in obs_list[N_copies+6+N_qc].split()]
      time[i_obs]           = time_tmp[1]+time_tmp[0]/86400.0
      # Add rank computation
      if is_post:
         obsvalue = obs[i_obs,0]
         sampling_noise  = np.random.normal(scale=np.sqrt(obs[i_obs,N_copies]),size=N_members)
         obs_mem_prio = obs[i_obs,5:-1:2]
         ensemble_values = np.sort(obs_mem_prio+sampling_noise)
         if obsvalue>ensemble_values[-1]:
            obs_rank[i_obs] = N_members
         else:
            obs_rank[i_obs] = np.where(obsvalue<ensemble_values)[0][0]
      else:
         obs_rank='none'

   # Arrange data
   obs = np.ma.masked_where(obs==-888888.0,obs)
   loc[:,0]=loc[:,0]*180/np.pi
   loc[loc[:,0]>180,0]=loc[loc[:,0]>180,0]-360
   loc[:,1]=loc[:,1]*180/np.pi

   # Create netcdf
   _make_netcdf_obs(file_obs+'.nc',N_obs,N_copies,N_qc,file_obs,CopyMetaData,QCMetaData,ObsTypesMetaData,obs,qc,obs_type,loc,vert,time,obs_rank,is_post)

   # Close file
   fid.close()   


def _read_dart_1obs_list(fid):
   obs_list = []
   string='notOBS'
   while string != 'OBS':
      obs_list.append(fid.readline())
      if not obs_list[-1]:
         string = 'OBS'
      else:
         string=obs_list[-1].split()[0]
   return obs_list

def _make_netcdf_obs(filename,N_obs,N_copies,N_qc,file_obs,CopyMetaData,QCMetaData,ObsTypesMetaData,obs,qc,obs_type,loc,vert,time,obs_rank,is_post):

   # NetCDF parameters
   dimensions =  collections.OrderedDict([\
      ('ObsIndex',N_obs),\
      ('copy',N_copies+1),\
      ('qc_copy',N_qc),\
      ('location',3)])
   attributes = collections.OrderedDict([\
      ('author','Romain Escudier'),\
      ('creation_date',dtime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),\
      ('source',file_obs),\
      ('CopyMetaData',CopyMetaData),\
      ('QCMetaData',QCMetaData),\
      ('ObsTypesMetaData',ObsTypesMetaData)])
   # Prepare netCDF
   nc_file = rt_netcdf_tools.nc_object(attributes,dimensions)
   # Define variables attributes
   obs_att=collections.OrderedDict([\
      ('long_name','org observation, estimates, etc.'),\
      ('explanation','see CopyMetaData'),\
      ('_FillValue',1e36)])
   qc_att=collections.OrderedDict([\
      ('long_name','QC values'),\
      ('explanation','see QcMetaData')])
   loc_att=collections.OrderedDict([\
      ('description','location coordinates'),\
      ('location_type','loc3Dsphere'),\
      ('long_name','threed sphere locations: lon, lat, vertical'),\
      ('storage_order','Lon Lat Vertical'),\
      ('units','degrees degrees which_vert')])
   vert_att=collections.OrderedDict([\
      ('long_name','vertical coordinate system code'),\
      ('VERTISUNDEF',-2),\
      ('VERTISSURFACE',-1),\
      ('VERTISLEVEL',1),\
      ('VERTISPRESSURE',2),\
      ('VERTISHEIGHT',3),\
      ('VERTISSCALEHEIGHT',4)])
   typ_att=collections.OrderedDict([\
      ('long_name','DART observation type'),\
      ('explanation','see ObsTypesMetaData')])
   tim_att=collections.OrderedDict([\
      ('long_name','time of observation'),\
      ('units','days since 1601-1-1'),\
      ('calendar','GREGORIAN')])
   if is_post:
      rank_att=collections.OrderedDict([\
         ('long_name','rank of observations')])
   # Create variables
   nc_file.add_variable('observations',obs,vardim=('ObsIndex','copy'),varatt=obs_att)
   nc_file.add_variable('qc',qc,vardim=('ObsIndex','qc_copy'),varatt=qc_att)
   nc_file.add_variable('location',loc,vardim=('ObsIndex','location'),varatt=loc_att)
   nc_file.add_variable('which_vert',vert,vardim=('ObsIndex'),varatt=vert_att)
   nc_file.add_variable('obs_type',obs_type,vardim=('ObsIndex'),varatt=typ_att)
   nc_file.add_variable('time',time,vardim=('ObsIndex'),varatt=tim_att)
   if is_post:
      nc_file.add_variable('obs_rank',obs_rank,vardim=('ObsIndex'),varatt=rank_att)
   # Create file
   nc_file.create_file(filename)
































