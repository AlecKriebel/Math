#!/usr/bin/env python3
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];df=pd.read_csv(ROOT/'data'/'figure_source_data'/'asymptotics.csv')
fig,ax=plt.subplots(figsize=(6.5,4.8),constrained_layout=True)
ax.plot(df.m,df.diffusion_ratio,label=r'$d_{\max}/d_{\min}$')
ax.set_xlabel('$m=n-1$');ax.set_ylabel('diffusion ratio');ax.set_title('Linear growth of the exact diffusion contrast');ax.legend(frameon=False)
fig.savefig(ROOT/'figures'/'asymptotic_scaling.pdf',bbox_inches='tight');fig.savefig(ROOT/'figures'/'asymptotic_scaling.png',dpi=180,bbox_inches='tight')
