#!/usr/bin/env python
import os,sys,pdb,scipy,glob
from pylab import *
from strolger_util import util as u
from scipy.optimize import curve_fit as cf

def line_x(x,*p):
    m,b=p
    return(m*x+b)

def read_fits_to_table(fits_file, verbose=True):
    from astropy.table import Table
    table = Table.read(fits_file)
    df = table.to_pandas()
    print('%s df read\n' %fits_file)
    return(df)

if __name__=='__main__':
    

    file = '../strolger-sn1a/analysis/ALLSFH_new_z/Cami_GOODS-N_zbest.dat'
    data = loadtxt(file)
    data[data==-99.]=np.nan
    idx = where(data[:,1]==8.0)
    data[idx[0]]=float('nan')

    ax1 = subplot(111)
    N1, bins, j1 = ax1.hist(data[:,1], alpha=0.4, bins=30, label='Pacifici16')
    (mx,mbins)=u.binmode(data[:,1], bins=30)
    ax1.axvline(mx, linestyle='-', color='C0', label='%2.2f' %(mx), alpha=0.4)

    df=read_fits_to_table('../ADAP_2021/pre_analysis/hlsp_candels_hst_wfc3_goodsn-barro19_multi_v1_mass-fast-cat.fits')
    N3, bins, j3 = ax1.hist(df['lmass'], alpha=0.4, bins=100, label='Barro19')
    (mx,mbins)=u.binmode(df['lmass'], bins=100)
    ax1.axvline(mx, linestyle='-', color='C1', label='%2.2f' %(mx), alpha=0.4)
    


    
    ax1.set_xlabel('log10(M)')
    ## ax2.set_ylabel('logMt_50')
    ax1.legend()
    ## ax2.legend()
    ax1.set_xlim(7.8,12.2)
    ## ax2.set_xlim(7.8,12.2)
    
    savefig('mass_comparison_v2.png')
    
    
