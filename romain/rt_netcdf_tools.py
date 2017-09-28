# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 16:21:43 2016

@author: romain
"""

import numpy as np
import netCDF4 as ncdf
import collections

#%%

class nc_variable:
    
    def __init__(self,varvalue,vartype,vardim,varatt):
        self.type  = vartype
        self.value = varvalue
        self.dimensions  = vardim
        self.attributes   = varatt

    def __repr__(self):
        if self.dimensions:
            print_dim='('
            for dimname in self.dimensions:
                print_dim=print_dim+dimname+', '
            print_dim=print_dim[0:-2]+')'
        else:
            print_dim=''
        return "NetCDF4 variable : "+self.type+print_dim


class nc_object:

    def __init__(self,globalatt=collections.OrderedDict(),dimensions=collections.OrderedDict()):
        self.attributes = globalatt
        self.dimensions = dimensions
        self.variables = collections.OrderedDict()

    def add_variable(self,varname,varvalue,vartype='double',vardim=(),varatt=collections.OrderedDict()):
        self.variables[varname] = nc_variable(varvalue,vartype,vardim,varatt)
        
    def nc_dump(self):
        print '#################################################'
        print 'dimensions:'
        for name, value in self.dimensions.items():
            print '\t '+name+' = '+str(value)+';'
        print 'variables:'
        for name, var in self.variables.items():
            if var.dimensions:
                print_dim='('
                for dimname in var.dimensions:
                    print_dim=print_dim+dimname+', '
                print_dim=print_dim[0:-2]+')'
                print '\t '+var.type+' '+name+''+print_dim+' ;'
            else:
                print '\t '+var.type+' '+name+' ;'
            for attname, attvalue in var.attributes.items():
                print '\t \t '+name+':'+attname+' = '+self.__num2str__(attvalue)+' ;'
        print ' '
        print '// global attributes:'
        for name, value in self.attributes.items():
            print '\t :'+name+' = '+self.__num2str__(value)+';'
        print '#################################################'
    
    def create_file(self,filename,format='NETCDF3_64BIT'):
        # Formats are NETCDF3_CLASSIC, NETCDF3_64BIT, NETCDF4_CLASSIC and NETCDF4
        file_nc = ncdf.Dataset(filename, 'w', format=format)
        
        # Global attributes
        for attname, attvalue in self.attributes.items():
            setattr(file_nc, attname, attvalue)
        
        # Create dimensions
        for name, value in self.dimensions.items():
            file_nc.createDimension(name, value)
        
        # Create variables
        for name, var in self.variables.items():
            print name
            nc_type = __nc_type__(var.type)
            try:
                fill_value=var.attributes['_FillValue']
            except KeyError:
                fill_value=None
            var_tmp = file_nc.createVariable(name, nc_type, var.dimensions,fill_value=fill_value)
            for attname, attvalue in var.attributes.items():
                if attname != '_FillValue':
                   setattr(var_tmp, attname, attvalue)
            var_tmp[:]=var.value
        
        # Close netCDF
        file_nc.close()
        print filename


    def __num2str__(self,value):
        if isinstance(value, basestring):
            return '"'+value+'"'
        else:
            return str(value)

    def __repr__(self):
        print_string = "NetCDF object\n"
        print_string = print_string+'dimensions:\n'
        for name, value in self.dimensions.items():
            print_string = print_string +'\t'+name+' = '+str(value)+' ;\n'
        print_string = print_string+ 'variables:\n'
        for name, var in self.variables.items():
            if var.dimensions:
                print_dim=' ('
                for dimname in var.dimensions:
                    print_dim=print_dim+dimname+', '
                print_dim=print_dim[0:-2]+')'
                print_string = print_string+ '\t'+name+print_dim+' ;\n'
            else:
                print_string = print_string+ '\t'+name+' ;\n'
        print_string = print_string+ 'global attributes:\n'
        for name, value in self.attributes.items():
            print_string = print_string+ '\t:'+name+' = '+self.__num2str__(value)+';\n'
        return print_string
        
def get_nc_object(filename):
    file_nc = ncdf.Dataset(filename, 'r')
    
    # Global attributes
    globatt=collections.OrderedDict()
    for name in file_nc.ncattrs():
        globatt[name] = file_nc.getncattr(name)

    # Get dimensions
    dimensions=collections.OrderedDict()
    for name, dims in file_nc.dimensions.items():
        dimensions[str(name)] = dims.size

    # Create object
    my_netcdf = nc_object(globatt,dimensions)

    # Get variables
    for name, var in file_nc.variables.items():
        varatt=collections.OrderedDict()
        for attname in var.ncattrs():
            varatt[attname] = var.getncattr(attname)
        vardim=()
        for dimname in var.dimensions:
            vardim = vardim + (str(dimname),)
        vartype=__nc_type_inv__(var.datatype)
        my_netcdf.add_variable(str(name),var[:],\
         vardim=vardim,varatt=varatt,vartype=vartype)

    # Close netCDF
    file_nc.close()
    
    return my_netcdf


def __nc_type__(vartype):
    nc_types={'double':'f8','single':'f4','integer':'i4','char':'S1'}
    try:
        return nc_types[vartype]
    except KeyError:
        print "Warning! Not a valid variable type. Using double..."
        return 'f8'
      
def __nc_type_inv__(vartype):
    nc_types={np.dtype('float64'):'double',\
              np.dtype('float32'):'single',\
              np.dtype('int32'):'integer',\
              np.dtype('S1'):'char'}
    try:
        return nc_types[vartype]
    except KeyError:
        print "Warning! Not a valid variable type. Using double..."
        return 'double'
      











