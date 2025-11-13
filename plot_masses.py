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

    ax1 = subplot(211)
    N1, bins, j1 = ax1.hist(data[:,1], alpha=0.4, bins=30, label='logM_50')
    (mx,mbins)=u.binmode(data[:,1], bins=30)
    ax1.axvline(mx, linestyle='-', color='C0', label='%2.2f' %(mx), alpha=0.4)
    
    N2, bins, j2 = ax1.hist(data[:,2], alpha=0.4, bins=30, label='logMt_50')
    (mx,mbins)=u.binmode(data[:,2], bins=30)
    ax1.axvline(mx, linestyle='-', color='C1', label='%2.2f' %(mx), alpha=0.4)


    ax2 = subplot(212)
    ax2.plot(data[:,1],data[:,2], '.')
    xx = arange(7.5,12.5,0.05)
    p0=[1,0]
    ax2.plot(xx,line_x(xx,*p0),'-',label='$y=%.1f x + %.1f$' %(p0[0], p0[1]))

    idx = ~(np.isnan(data[:,1]) | np.isnan(data[:,2]))
    popt,pcov=cf(line_x,data[idx][:,1],data[idx][:,2],p0=p0,check_finite=False)
    ax2.plot(xx,line_x(xx,*popt),'-',label='$y=%.1f x + %.1f$' %(popt[0], popt[1]))
    print (popt)
    
    ax2.set_xlabel('logM_50')
    ax2.set_ylabel('logMt_50')
    ax1.legend()
    ax2.legend()
    #ax1.set_xlim(7.8,12.2)
    ax2.set_xlim(7.8,12.2)
    
    savefig('mass_comparison.png')
    
    
