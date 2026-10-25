#!/usr/bin/env python3
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams.update({'pdf.fonttype': 42, 'ps.fonttype': 42})
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/'data'/'branch_amplitudes.csv');df=df[(df.modes==16)&(df.precision=='base')]
fig,ax=plt.subplots(figsize=(6.3,4.6),constrained_layout=True)
for m,g in df.groupby('m'):
    ax.plot(g.predicted_amplitude,g.measured_amplitude,'o-',label=f'$m={m}$')
lo=min(df.predicted_amplitude.min(),df.measured_amplitude.min());hi=max(df.predicted_amplitude.max(),df.measured_amplitude.max());ax.plot([lo,hi],[lo,hi],linestyle='--',linewidth=1,label='normal-form equality')
ax.set_xlabel(r'predicted $\sqrt{-\eta_m\mu/c_m}$');ax.set_ylabel('measured adjoint-projected amplitude');ax.set_title('First-mode amplitude near onset');ax.legend(frameon=False)
fig.savefig(ROOT/'figures'/'amplitude_scaling.pdf',bbox_inches='tight');fig.savefig(ROOT/'figures'/'amplitude_scaling.png',dpi=180,bbox_inches='tight')
