
import numpy as np

def rms(X,dim):
   """
   Root mean square of an array along one dimension
   """
   siz = np.shape(X)
   my_rms=np.sqrt(np.sum(np.square(X),axis=dim))/np.sqrt(siz[dim]-1)
   return my_rms

def loess(data,fc,t=np.nan,t_final=np.nan,step=1):
   """
   Loess filtering of a time serie
   """
   # Initialize
   if np.isnan(t):
      t       = np.arange(0,len(data)*step,step)
   if np.isnan(t_final):
      t_final = np.arange(0,len(data)*step,step)
   tau = 1./fc   
   data_smooth = np.ones(len(t_final))*np.nan

   # Only compute for the points where t_final is in the range of t
   sx = (t_final >= np.min(t)) & (t_final <= np.max(t))

   # Loop on desired points
   for i in np.arange(len(t_final))[sx]:
      dn = np.abs(t-t_final[i])/tau
      idx_weights = dn<1
      n_pts = idx_weights.sum()
      if (n_pts > 3):
         dn = dn[idx_weights]
         w = (1-dn*dn*dn)
         weights = w*w*w
         X = np.array([np.ones(n_pts),t[idx_weights],t[idx_weights]**2]).transpose()
         W = np.diag(weights)
         B,resid,rank,s = np.linalg.lstsq(np.dot(W,X),np.dot(W,data[idx_weights]))
         data_smooth[i] = B[0]+B[1]*t_final[i]+B[2]*t_final[i]**2
   return data_smooth

def gc_dist(lon1,lat1,lon2,lat2):
   """
   Distance between 2 vector points along a great circle
   """
   lon1 = (np.pi/180.) * lon1
   lon2 = (np.pi/180.) * lon2
   lat1 = (np.pi/180.) * lat1
   lat2 = (np.pi/180.) * lat2

   dlat = lat2-lat1
   dlon = lon2-lon1

   #haversine function
   dang = 2*np.arcsin( np.sqrt( np.sin(dlat/2)**2 + np.cos(lat2)*np.cos(lat1)*np.sin(dlon/2)**2 ) )

   r_earth = 6371315.

   return r_earth*dang

def gc_dist_diff(lon,lat):
   """
   Distance between the points of a vector points along a great circle
   """
   lon1 = lon[0:-1]
   lat1 = lat[0:-1]
   lon2 = lon[1:]
   lat2 = lat[1:]

   return gc_dist(lon1,lat1,lon2,lat2)


