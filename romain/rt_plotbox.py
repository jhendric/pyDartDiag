# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 15:41:14 2016

@author: romain
"""

import numpy as np
import matplotlib.colors
import matplotlib.pylab as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap
import math



def rt_plot_2D( lon,lat,var,\
                geo=[-98, -45, 10, 52],clim=[float('nan') ,1],cstep=50,pal=cm.gist_ncar,\
                coastcolor=[.9,.9,.9],coastlinecolor=[.5,.5,.5],lakecolor=[1,1,1],
                plotitle='',subpltid=111,fontsiz=16,colorbar=True,stepX=10.,stepY=10.):
     """
     Plot a map with 2D field
     """    
    # Initialize
    if not var.any():
        is_plot=False
    else:
        is_plot=True
    if (math.isnan(clim[0]) and is_plot):
        clim = [np.min(var[:]),np.max(var[:])];
    if not isinstance(cstep,float):
        cstep=(clim[1]-clim[0])/float(cstep)
    # Create figure
    fig=plt.gcf()
    if isinstance(subpltid,tuple):
       ax  = fig.add_subplot(subpltid[0],subpltid[1],subpltid[2])
    else:
       ax  = fig.add_subplot(subpltid)
    # Create projection
    m = Basemap(projection='cyl',llcrnrlon=geo[0],urcrnrlon=geo[1],\
                llcrnrlat=geo[2],urcrnrlat=geo[3],\
                resolution='l')
    # Draw coast
    m.drawcoastlines(color=coastlinecolor)
    m.fillcontinents(color=coastcolor,lake_color=lakecolor)
    # Grid
    parallels = np.arange(0.,60.,stepY)
    m.drawparallels(parallels,labels=[True,False,False,True],fontsize=fontsiz,color=[.6,.6,.6]) # labels = [left,right,top,bottom]
    meridians = np.arange(-100.,-30.,stepX)
    m.drawmeridians(meridians,labels=[False,False,False,True],fontsize=fontsiz,color=[.6,.6,.6]) # labels = [left,right,top,bottom]
    # contour filled
    if is_plot:
        norm = matplotlib.colors.Normalize(vmin=clim[0], vmax=clim[1])
        contours = np.arange(clim[0],clim[1]+cstep,cstep)
        C = m.contourf(lon,lat,var,contours,cmap=pal,norm=norm,extend='both')
        # colorbar
        if colorbar:
            cbar = plt.colorbar(C,orientation='horizontal',shrink=0.8)
            cbar.ax.tick_params(labelsize=fontsiz) 
    # title
    plt.title(plotitle,fontsize=fontsiz+2)

    return m

def xaxis_date(fds,step=1,ax=0,date_format='%Y/%m/%d'):
     """
     Put dates on X-axis
     """
    #from matplotlib.ticker import AutoMinorLocator
    import matplotlib.dates as mpl_dates
    try:
       ax.xaxis
    except :
       ax=plt.gca()
    if (step == 'month'):
       datevec = mpl_dates.num2date(fds)
       datetick = []
       for i in xrange(len(datevec)):
          if datevec[i].day == 1:
             datetick.append(datevec[i])
       fdstick = mpl_dates.date2num(datetick)
    elif (step == 'year'):
       datevec = mpl_dates.num2date(fds)
       datetick = []
       for i in xrange(len(datevec)):
          if (datevec[i].day == 1 & datevec[i].month == 1):
             datetick.append(datevec[i])
       fdstick = mpl_dates.date2num(datetick)
    else:
       fdstick = fds[::step]
    hfmt = mpl_dates.DateFormatter(date_format) # matplotlib date format object
    ax.xaxis.set_major_formatter(hfmt)
    ax.xaxis.set_ticks(fdstick)
    #minor_locator = AutoMinorLocator(step)
    #ax.xaxis.set_minor_locator(minor_locator)



def rt_getcolormaps(file_cb='/Users/romain/Work/Tools/IMEDEA/Matlab/Matlab-toolbox/Plot/rt_colormaps.txt'):
    rt_colormaps = dict()
    # Open file
    curr = 0
    with open(file_cb,'r') as f:
        for line in f:
            i_tmp=np.mod(curr,4)
            if (i_tmp==0):
                # The first line is the name of the colormap
                if curr>0:
                    # If not on the first line of file, save previous cm
                    rt_colormaps[name] = cmat2cmpl(val);
                    del(val)
                name=line.strip()
            else:
                # get values of colormap
                line=line.strip()
                cols = line.split(',')
                # if Red values (first column), initialize array
                if (i_tmp == 1):
                    val=np.zeros([3,len(cols)-1])
                val[i_tmp-1,:]=[float(y) for y in cols[0:-1]]
            curr+=1
    return rt_colormaps


def cmat2cmpl(colormap): 
     """ 
     Convert matlab style colormap to matplotlib style 
     Enter a list non normalized RGB values from 0-255 
     """ 
     r = colormap[0,:]
     g = colormap[1,:]
     b = colormap[2,:]
     cmap = matplotlib.colors.ListedColormap(zip(r,g,b)) 
     return cmap 

def cmpl2cmat(cmap):
     """
     Convert matplotlib style colormap to matlab style
     Enter a matplotlib colormap
     """
     colormap=np.transpose(np.array([list(cmap(i/(cmap.N-1.))) for i in xrange(cmap.N)])[:,0:3])
     return colormap


def set_plt_fontsize(ax,fontsiz):
     """ 
     Change fontsize of given plot
     """ 
     for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
         item.set_fontsize(fontsiz)

def rt_getcolors(file_col='/Users/romain/Work/Tools/IMEDEA/Matlab/Matlab-toolbox/Plot/rt_colors.txt'):
    rt_colors = dict()
    # Open file
    with open(file_col,'r') as f:
        for line in f:
            cols=line.strip().split(',')
            rt_colors[cols[0]] = (float(cols[1]),float(cols[2]),float(cols[3]))
    return rt_colors


def pale_color(color,perc=0.3):
    col_pale=[0,0,0]
    for i in xrange(3):
        inc=(1-color[i])*perc
        col_pale[i]=min(1,color[i]+inc)
    return col_pale


def pale_cmap(cmap,perc=0.3):
    colormap      =cmpl2cmat(cmap)
    colormap_pale = np.empty(colormap.shape)
    for i in xrange(colormap.shape[1]):
        colormap_pale[:,i] = pale_color(colormap[:,i],perc=perc)
    cmap_pale = cmat2cmpl(colormap_pale)
    return cmap_pale 



