
print('----------------------------------------------------------------')
print('                        Dart Obs to netcdf                      ')
print('----------------------------------------------------------------')

#%% Toolboxes

from param_dart import *
import rt_netcdf_tools
import collections

#%% Conversion

for filename in glob.iglob(dir_obs+'/obs_seq*'):
   file_base, file_ext = os.path.splitext(filename)
   if file_ext != '.nc':
      if not os.path.isfile(filename+'.nc'):
         rt_dart_tools.read_dart_obs_analysis(filename)













