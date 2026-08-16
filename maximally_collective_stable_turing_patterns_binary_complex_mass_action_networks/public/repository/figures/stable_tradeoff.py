#!/usr/bin/env python3
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
fig,ax=plt.subplots(figsize=(6.9,4.7),constrained_layout=True)
for m in (3,5,8,12):
    r=m-2
    L0=1/np.sqrt(3*r);L1=90*r/(90*r+1)
    L=np.linspace(L0,L1,240)
    chiD=(23/63)*91*r*L
    chiH=(91*r-1)/(91*r*L)
    x=np.linspace(max(1,np.sqrt(8*r)/3),max(chiD)*1.04,240)
    ax.plot(chiD,chiH,label=fr'certified stable, $m={m}$')
    ax.plot(x,8*r/x,linestyle='--',linewidth=.9)
    ax.scatter([(23/(63*np.sqrt(3)))*91*np.sqrt(r)],
               [np.sqrt(3*r)*(91*r-1)/(91*r)],s=22)
ax.set_xscale('log');ax.set_yscale('log')
ax.set_xlabel(r'diffusion contrast $\chi_D$')
ax.set_ylabel(r'equilibrium contrast $\chi_H$')
ax.set_title('Exact stable trade-offs and universal lower hyperbolas')
ax.legend(frameon=False,fontsize=7.4,ncol=2)
ax.text(.02,.02,r'Dashed: $\chi_D\chi_H=8(m-2)$'+'\nDots: square-root-balanced endpoints',transform=ax.transAxes,fontsize=7.5)
fig.savefig(ROOT/'figures'/'stable_tradeoff.pdf',bbox_inches='tight')
fig.savefig(ROOT/'figures'/'stable_tradeoff.png',dpi=180,bbox_inches='tight')
