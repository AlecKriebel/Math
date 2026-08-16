#!/usr/bin/env python3
from pathlib import Path
import json
import pandas as pd
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data'/'simulations'
fig,ax=plt.subplots(figsize=(7.0,4.6),constrained_layout=True)
for m in (3,5,8):
    candidates=sorted(DATA.glob(f'profile_m{m}_mu0p005_K*_*.csv'))
    if not candidates:
        continue
    preferred=[p for p in candidates if 'spatial-fine' in p.name]
    p=preferred[-1] if preferred else candidates[-1]
    df=pd.read_csv(p)
    meta_path=DATA/p.name.replace('profile_','parameters_').replace('.csv','.json')
    meta=json.load(open(meta_path))
    pred=meta['predicted_amplitude']; meas=abs(meta['measured_amplitude'])
    ax.plot(df['x'],(df['X1']-1)/pred,label=fr'$m={m}$, measured/predicted $={meas/pred:.3f}$')
ax.axhline(0,linestyle=':',linewidth=.8)
ax.set_xlabel(r'position $\xi$')
ax.set_ylabel(r'normalized $X_1$ deviation $(X_1-1)/A_{\rm pred}$')
ax.set_title('Numerical illustrations of the rigorously proved stable branches')
ax.legend(frameon=False,fontsize=8)
fig.savefig(ROOT/'figures'/'stable_profiles.pdf',bbox_inches='tight')
fig.savefig(ROOT/'figures'/'stable_profiles.png',dpi=180,bbox_inches='tight')
