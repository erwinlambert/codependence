import numpy as np
import xarray as xr

def models():
    return ['bcc-csm1-1','CanESM2','CCSM4','CNRM-CM5','CSIRO-Mk3-6-0','GFDL-CM3','GISS-E2-R','HadGEM2-ES','inmcm4','IPSL-CM5A-LR','MIROC-ESM','MIROC5','MPI-ESM-LR','MRI-CGCM3','NorESM1-M']

def addrest(time,SLR):
    #ADD GIA
    
    #ADD LWS
    
    #ADD GDYN
    return time,SLR

def loadslr(model,scen):
    #Load model-specific components
    with xr.open_dataset(f'../data/rsl/{model}_{scen}.nc') as ds:
        SLR  = ds['SLR_lt'].values
        time = ds['time_lt'].values

    #Add model-independent components
    time,SLR = addrest(time,SLR)
    
    return time,SLR
