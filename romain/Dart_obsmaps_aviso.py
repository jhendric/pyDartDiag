# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 14:31:01 2016

@author: romain
"""

print('----------------------------------------------------------------')
print('                        Post-processing Obs Dart                ')
print('----------------------------------------------------------------')

#%% Toolboxes

from param_dart import *
from matplotlib.colors import Normalize
import matplotlib.patches as patches
import subprocess

# Create palette for rank
pal_tmp=rt_plotbox.cmpl2cmat(rt_plotbox.pale_cmap(rt_colormaps['redblueclass'],perc=0.6))
pal_tmp2=rt_plotbox.cmpl2cmat(rt_colormaps['redblueclass'])
pal=np.empty((pal_tmp.shape[0],pal_tmp.shape[1]+2))
pal[:,1:-1]=pal_tmp; pal[:,0]=pal_tmp2[:,0]; pal[:,-1]=pal_tmp2[:,-1]
pal=rt_plotbox.cmat2cmpl(pal)

marker_size=20

#%% Observations

for dday in datevec_assim:
    figname=dir_pictures + '/Obs_seq_aviso_' + simu + '_' + dday.strftime('%Y%m%d')
    if not os.path.isfile(figname+'.jpg'):
        # Get data
        file_obs = glob.glob(dir_obs+'obs_seq.aviso.final.'+dday.strftime('%Y%m%d')+'.nc')[0];
        nc_obs = ncdf.Dataset(file_obs,'r')
        
        obs_lon     = np.array(nc_obs.variables['location'])[:,0]
        obs_lat     = np.array(nc_obs.variables['location'])[:,1]
        obs_val     = np.array(nc_obs.variables['observations'])[:,0]*100
        obs_prior   = np.array(nc_obs.variables['observations'])[:,1]*100
        obs_reana   = np.array(nc_obs.variables['observations'])[:,2]*100
        obs_spread  = np.array(nc_obs.variables['observations'])[:,3]*100
        obs_qc      = np.array(nc_obs.variables['qc'])[:,1]
        obs_type    = np.array(nc_obs.variables['obs_type'])[:]
        obs_rank    = np.array(nc_obs.variables['obs_rank'])[:]
        
        nc_obs.close()
        
        # Remove NaNs
        obs_prior[obs_prior>1000]=float('nan')
        obs_reana[obs_reana>1000]=float('nan')
        obs_spread[obs_spread>1000]=float('nan')
        

        fig = plt.figure(figsize=[20.,20.])
        plt.clf()
        # Plot observations
        m=rt_plotbox.rt_plot_2D(np.array([]),np.array([]),np.array([]),subpltid=321,fontsiz=14,plotitle='Observations')
        p=m.scatter(obs_lon, obs_lat, c=obs_val,edgecolors='none',s=20,cmap=rt_colormaps['intense2'])
        cb=m.colorbar(pad="8%")
        clip=p.get_clim()
        # Plot mean of reanalysis
        m=rt_plotbox.rt_plot_2D(np.array([]),np.array([]),np.array([]),subpltid=322,fontsiz=14,plotitle='Reanalysis')
        m.scatter(obs_lon, obs_lat, c=obs_reana,edgecolors='none',s=20,cmap=rt_colormaps['intense2'],\
                  vmin=clip[0],vmax=clip[1])
        cb=m.colorbar(pad="8%")
        # Plot innovation
        m=rt_plotbox.rt_plot_2D(np.array([]),np.array([]),np.array([]),subpltid=323,fontsiz=14,plotitle='Innovation')
        m.scatter(obs_lon, obs_lat,c=obs_val-obs_prior,edgecolors='none',s=marker_size,\
                  cmap=rt_colormaps['redblueclass'],vmin=-200,vmax=200)
        cb=m.colorbar(pad="8%")
        # Plot spread
        m=rt_plotbox.rt_plot_2D(np.array([]),np.array([]),np.array([]),subpltid=324,fontsiz=14,plotitle='Spread')
        norm = Normalize(vmin=0., vmax=200)
        m.scatter(obs_lon, obs_lat, c=obs_spread,edgecolors='none',s=marker_size,cmap=rt_colormaps['eke2'],norm=norm)
        cb=m.colorbar(pad="8%")
        # Plot rank
        m=rt_plotbox.rt_plot_2D(np.array([]),np.array([]),np.array([]),subpltid=325,fontsiz=14,plotitle='Rank of observation')
        norm = Normalize(vmin=0., vmax=30)
        m.scatter(obs_lon, obs_lat, c=obs_rank,edgecolors='none',s=marker_size,\
                  cmap=pal,norm=norm)
        cb=m.colorbar(pad="8%")
        # Plot QC
        m=rt_plotbox.rt_plot_2D(np.array([]),np.array([]),np.array([]),subpltid=326,fontsiz=14,plotitle='Dart QC')
        scat=m.scatter(obs_lon, obs_lat, c=obs_qc,edgecolors='none',s=marker_size)
        ax = plt.gca()
        ax.add_patch(patches.Rectangle((-1000, 0), 0.5, 0.5,facecolor=scat.cmap(0), label='Assimilated'))
        ax.add_patch(patches.Rectangle((-1000, 0), 0.5, 0.5,facecolor=scat.cmap(0.94),  label='Rejected'))
        ax.add_patch(patches.Rectangle((-1000, 0), 0.5, 0.5,facecolor=scat.cmap(4./7),label='Out of domain'))
        plt.legend(loc=4)
        cb=m.colorbar(pad="8%")

        plt.tight_layout()
        plt.savefig(figname+'.png')
        plt.close(fig)
        os.system('convert '+figname+'.png'+' '+figname+'.jpg')
        os.system('rm '+figname+'.png')

        print(figname+'.jpg')















 
