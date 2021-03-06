#!/usr/bin/env python
import os,sys,pdb,scipy,glob,pickle
from pylab import *
from strolger_util import util as u
from scipy.stats import gaussian_kde
from random import sample

if __name__=='__main__':
    
    rcParams['figure.figsize']=20, 10
    rcParams['font.size']=24.0


    data_pkl = 'all_gxys.pkl'
    if not os.path.isfile(data_pkl):
        data_n = loadtxt('Cami_GOODS-N_zbest.dat')
        data_n[:,0]+=100000
        data_s = loadtxt('Cami_GOODS-S_zbest.dat')
        data_s[:,0]+=200000
        data=concatenate((data_n,data_s), axis=0)
        pickle.dump(data,open(data_pkl,'wb'))
    else:
        data=pickle.load(open(data_pkl,'rb'))
        
    ### cols-- 0=id, 1=logM, 3=log_SFR, 7=redshift

    #pdb.set_trace()

    data[data==-99.]=np.nan
    idx = where(data[:,1]==8.0)
    data[idx[0]]=float('nan')
    idx = where(data[:,3]==-3.0)
    data[idx[0]]=float('nan')
    idx = where(data[:,7]==6.0)
    data[idx[0]]=float('nan')

    ## and to get rid of stars
    """
    This is tricky as the info for CLASS_STAR
    is in a separate set of files
    """
    junk_pkl = 'junk.pkl'
    if not os.path.isfile(junk_pkl):
        j1 = loadtxt('CANDELS_GDSN_znew_avgal_radec.dat')
        j2 = loadtxt('CANDELS_GDSS_znew_avgal_radec.dat')
        j1 = np.delete(j1,[38,39],1) ## remove the extra phot columns 

        j1[:,0] = j1[:,0]+100000
        j2[:,0] = j2[:,0]+200000
        junk = concatenate((j1,j2), axis=0)
        pickle.dump(junk,open(junk_pkl,'wb'))
    else:
        junk=pickle.load(open(junk_pkl,'rb'))
        
    idx = where(junk[:,-3]>=0.8)
    data[idx[0]]=float('nan')

    fig = plt.figure()
    gs = GridSpec(4,4)

    ax1 = fig.add_subplot(gs[1:4,0:3])
    ax2 = fig.add_subplot(gs[0,0:3], sharex=ax1)
    ax3 = fig.add_subplot(gs[1:4,3], sharey=ax1)

    Y = data[:,1][~isnan(data[:,1])]
    X = data[:,7][~isnan(data[:,7])]


    # fit an array of size [Ndim, Nsamples]
    tmp = np.vstack([X, Y])
    kde = gaussian_kde(tmp)

    # evaluate on a regular grid
    ygrid = np.linspace(8.0, 12.,60)
    xgrid = np.linspace(0,6,60)
    Xgrid, Ygrid = np.meshgrid(xgrid, ygrid)
    Z = kde.evaluate(np.vstack([Xgrid.ravel(), Ygrid.ravel()]))
        
    ax1.imshow(Z.reshape(Xgrid.shape),
               origin='lower', aspect='auto',
               extent=[0,6, 8, 12],
           cmap='bone_r')

    cs1 = ax1.contour(Xgrid, Ygrid, Z.reshape(Xgrid.shape), [0.01, 0.05, 0.32], colors='black')
    fmt={}
    strs = ['3$\sigma$','2$\sigma$','1$\sigma$']
    for l, s in zip(cs1.levels, strs):
        fmt[l]=s
    plt.clabel(cs1, cs1.levels, inline=1, fmt=fmt)


    ax2.hist(X, bins=100,  color='0.5', density=True, label='All Catalog Galaxies')
    ax3.hist(Y, bins=60,  color='0.5', density=True, orientation='horizontal')



    idx = loadtxt('host_idxs.txt')
    mask = in1d(data[:,0], idx)
    data_ias = data[mask]
    
    ax1.plot(data_ias[:,7], data_ias[:,1], 'o', color='C3', ms=10)
    ax2.hist(data_ias[:,7], bins=10,  align='left', color ='C3', lw=3, histtype = 'step', density=True, label='SN Ia Hosts')
    ax3.hist(data_ias[:,1], bins=10,  color='C3', lw=3, histtype= 'step', density=True, orientation='horizontal')



    ax2.legend(loc=1, ncol=2, frameon=False, fontsize=20)

    ax1.set_xlim(0,6)
    #ax2.set_ylim(0,0.8)
    plt.setp(ax2.get_xticklabels(), visible=False)
    plt.setp(ax3.get_yticklabels(), visible=False)
    ax2.set_yticks([])
    ax3.set_xticks([])

    ax1.set_ylabel('Log (M/M$_{\odot}$)')
    ax1.set_xlabel('Redshift')
    
    savefig('figure_mass.png')


    clf()
    
    fig = plt.figure()
    gs = GridSpec(4,4)

    ax1 = fig.add_subplot(gs[1:4,0:3])
    ax2 = fig.add_subplot(gs[0,0:3], sharex=ax1)
    ax3 = fig.add_subplot(gs[1:4,3], sharey=ax1)

    Y = data[:,3][~isnan(data[:,3])]
    X = data[:,7][~isnan(data[:,7])]


    # fit an array of size [Ndim, Nsamples]
    tmp = np.vstack([X, Y])
    kde = gaussian_kde(tmp)

    # evaluate on a regular grid
    ygrid = np.linspace(-3.5,4,60)
    xgrid = np.linspace(0,6,60)
    Xgrid, Ygrid = np.meshgrid(xgrid, ygrid)
    Z = kde.evaluate(np.vstack([Xgrid.ravel(), Ygrid.ravel()]))
        
    ax1.imshow(Z.reshape(Xgrid.shape),
               origin='lower', aspect='auto',
               extent=[0,6, -3.5,4],
               #cmap=plt.cm.gist_earth_r)
               cmap='bone_r')

    #cs1 = ax1.contour(Xgrid, Ygrid, Z.reshape(Xgrid.shape), [0.01, 0.05, 0.32], colors='black')
    cs1 = ax1.contour(Xgrid, Ygrid, Z.reshape(Xgrid.shape), [0.0027, 0.05, 0.32], colors='black')
    fmt={}
    strs = ['3$\sigma$','2$\sigma$','1$\sigma$']
    for l, s in zip(cs1.levels, strs):
        fmt[l]=s
    plt.clabel(cs1, cs1.levels, inline=1, fmt=fmt)


    ax2.hist(X, bins=100,  color='0.5', density=True, label='All Catalog Galaxies')
    ax3.hist(Y, bins=60,  color='0.5', density=True, orientation='horizontal')

    ax1.plot(data_ias[:,7], data_ias[:,3], 'o', color='C3', ms=10)
    ax2.hist(data_ias[:,7], bins=10,  align='left', color ='C3', lw=3, histtype = 'step', density=True, label='SN Ia Hosts')
    ax3.hist(data_ias[:,3], bins=10,  color='C3', lw=3, histtype= 'step', density=True, orientation='horizontal')

    ax2.legend(loc=1, ncol=2, frameon=False, fontsize=20)

    ax1.set_xlim(0,6)
    #ax2.set_ylim(0,0.8)
    plt.setp(ax2.get_xticklabels(), visible=False)
    plt.setp(ax3.get_yticklabels(), visible=False)
    ax2.set_yticks([])
    ax3.set_xticks([])

    ax1.set_ylabel('Log (SFR)')
    ax1.set_xlabel('Redshift')
    
    savefig('figure_sfr.png')

    
