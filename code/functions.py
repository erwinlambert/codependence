import os,sys
import glob
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import scipy.stats as st
from scipy.io import loadmat

sourcedir = '/Volumes/My Passport/cmip5/cmip5'

def download(model,domain,var,scen):
    os.system(f'RSYNC_PASSWORD=getdata rsync -vrlpth cmip5user@atmos.ethz.ch::cmip5/{scen}/{domain}/{var}/{model}/r1i1p1/ /Volumes/My\ Passport/cmip5/cmip5/{model}/r1i1p1')

def models():
    return ['bcc-csm1-1','CanESM2','CCSM4','CNRM-CM5','CSIRO-Mk3-6-0','GFDL-CM3','GISS-E2-R','HadGEM2-ES','inmcm4','IPSL-CM5A-LR','MIROC-ESM','MIROC5','MPI-ESM-LR','MRI-CGCM3','NorESM1-M']
    
def detrend(VAR,VAR_pi,years):
    if len(VAR_pi)>0:
        years_pi = np.arange(0,len(VAR_pi))
        slope,intercept,rval,pval,stderr = st.linregress(years_pi,VAR_pi)
        VAR = VAR-slope*(years)
    #Reference to 1986-2005
    VAR = VAR-np.mean(VAR[np.logical_and(years>1985,years<2006)]) 
    return VAR

def saveSLR(SLR,years,model,scen,loc):
    SLR_lt = SLR.copy()
    time_lt = years.copy()
    
    #Extract common time period
    SLR = SLR_lt[np.logical_and(years>2005,years<2101)]
    time = time_lt[np.logical_and(years>2005,years<2101)]
    
    SLR_lt2 = xr.DataArray(SLR_lt,dims=('time_lt'),coords={'time_lt':time_lt})
    SLR2      = xr.DataArray(SLR,dims=('time'),coords={'time':time})
    ds = xr.Dataset({'SLR_lt':SLR_lt2,'SLR':SLR2})
    ds.to_netcdf(f'../data/{loc}/{model}_{scen}.nc')
    ds.close()
    
    print(scen,model,'Saved ',loc)

