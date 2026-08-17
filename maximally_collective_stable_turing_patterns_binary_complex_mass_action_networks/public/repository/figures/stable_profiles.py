#!/usr/bin/env python3
from pathlib import Path
import json
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams.update({'pdf.fonttype': 42, 'ps.fonttype': 42})
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'/'simulations'
fig,(ax1,ax2)=plt.subplots(1,2,figsize=(10.2,4.3),constrained_layout=True)
for m in (3,5,8):
    p=DATA/f'profile_m{m}_mu0p02_K32_spatial-fine.csv'
    if not p.exists():
        candidates=sorted(DATA.glob(f'profile_m{m}_mu0p02_K*_*.csv'))
        if not candidates: continue
        preferred=[q for q in candidates if 'spatial-fine' in q.name]
        p=preferred[-1] if preferred else candidates[-1]
    df=pd.read_csv(p)
    meta_path=DATA/p.name.replace('profile_','parameters_').replace('.csv','.json')
    meta=json.load(open(meta_path))
    pred=meta['predicted_amplitude']; meas=abs(meta['measured_amplitude'])
    ax1.plot(df['x'],(df['X1']-1)/pred,label=fr'$m={m}$, ratio $={meas/pred:.3f}$')
ax1.axhline(0,linestyle=':',linewidth=.8)
ax1.set_xlabel(r'position $\xi$')
ax1.set_ylabel(r'normalized deviation $(X_1-1)/A_{\rm pred}$')
ax1.set_title(r'(a) Stable profiles at $\mu=0.02$')
ax1.legend(frameon=False,fontsize=8)

amp=pd.read_csv(ROOT/'data'/'branch_amplitudes.csv')
amp=amp[(amp.modes==16)&(amp.precision=='base')]
for m,g in amp.groupby('m'):
    g=g.sort_values('mu')
    ratio=g.measured_amplitude/g.predicted_amplitude
    ax2.plot(g.mu,ratio,'o-',label=fr'$m={int(m)}$')
ax2.axhline(1,linestyle='--',linewidth=1,label='normal-form limit')
ax2.set_xscale('log')
ax2.invert_xaxis()
ax2.set_xlabel(r'bifurcation distance $\mu$ (decreasing $\rightarrow$)')
ax2.set_ylabel(r'measured / predicted amplitude')
ax2.set_title('(b) Convergence to the normal form')
ax2.legend(frameon=False,fontsize=8)
fig.suptitle('Numerical illustrations of the rigorously proved stable branches')
fig.savefig(ROOT/'figures'/'stable_profiles.pdf',bbox_inches='tight')
fig.savefig(ROOT/'figures'/'stable_profiles.png',dpi=180,bbox_inches='tight')
