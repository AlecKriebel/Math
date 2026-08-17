#!/usr/bin/env python3
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'pdf.fonttype': 42, 'ps.fonttype': 42})
ROOT=Path(__file__).resolve().parents[1]
fig,ax=plt.subplots(figsize=(6.9,4.7),constrained_layout=True)
markers=('o','s','^','D')
for idx,m in enumerate((3,5,8,12)):
    nu=m-2
    L0=1/np.sqrt(3) if nu==1 else np.sqrt(5/(4*nu))
    L1=90*nu/(90*nu+1)
    L=np.linspace(L0,L1,240)
    chiD=(23/63)*91*nu*L
    chiH=(91*nu-1)/(91*nu*L)
    x=np.linspace(max(1,np.sqrt(8*nu)/3),max(chiD)*1.04,240)
    line,=ax.plot(chiD,chiH,label=fr'certified stable, $m={m}$',
                  marker=markers[idx],markevery=48,markersize=3.5)
    color=line.get_color()
    ax.plot(x,8*nu/x,linestyle=':',linewidth=1.0,color=color,alpha=.82)
    ax.scatter([chiD[0]],[chiH[0]],s=35,color=color,marker=markers[idx],
               edgecolor='black',linewidth=.35,zorder=3)
ax.set_xscale('log');ax.set_yscale('log')
ax.set_xlabel(r'diffusion contrast $\chi_D$')
ax.set_ylabel(r'equilibrium contrast $\chi_H$')
ax.set_title('Exact stable trade-offs and universal lower hyperbolas')
ax.legend(frameon=False,fontsize=7.4,ncol=2)
ax.text(.02,.02,r'Dotted: $\chi_D\chi_H=8(m-2)$'+'\nMarked endpoints: certified square-root scaling',transform=ax.transAxes,fontsize=7.5)
fig.savefig(ROOT/'figures'/'stable_tradeoff.pdf',bbox_inches='tight')
fig.savefig(ROOT/'figures'/'stable_tradeoff.png',dpi=180,bbox_inches='tight')
