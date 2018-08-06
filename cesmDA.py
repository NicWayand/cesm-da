import os
import xarray as xr
import glob
import numpy as np

def load_run(username=None, casename=None, runname=None, Nens=None):
    ''' Loads in cice run data and returns a dataset.'''
    
    
    data_dir = os.path.join('/glade/scratch', username, casename, runname, 'run')
    ds_ens = []
    for ens in np.arange(1,Nens+1,1):
        all_files = sorted(glob.glob(os.path.join(data_dir,runname+'.cice_'+'{num:0{width}}'.format(num=ens, width=4)+'.h.*.nc')))
        if all_files:
            ds_ice_c = xr.open_mfdataset(all_files, autoclose=True, parallel=True, concat_dim='time')
            ds_ice_c['ensemble'] = ens
            ds_ens.append(ds_ice_c)
        else:
            print(glob.glob(os.path.join(data_dir,runname+'.cice_0008.h.*.nc')))
            raise ValueError("Found no files")
    ds_ice = xr.concat(ds_ens, dim='ensemble')
    
    return ds_ice