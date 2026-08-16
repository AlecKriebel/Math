#!/usr/bin/env python3
"""Exact and high-precision asymptotics for the all-spectrum family."""
from __future__ import annotations
import argparse, csv, math
from pathlib import Path
import sympy as sp
from closed_form import diffusion_entries, eta_formula, cubic_formula

HINF=sp.log(sp.Rational(227,224))/3
L_INF=sp.Rational(1860005,15369)
M_INF=sp.Rational(99148487,7377120)+sp.Rational(1860005,5123)*HINF
R_INF=sp.Rational(154272095910280246797682723,15463293371745820143206400)
C_INF=-sp.Rational(177254418741034502693,642248694666476448)
N_INF=R_INF+C_INF*HINF
ETA_INF=M_INF/L_INF
CUBIC_INF=N_INF/L_INF
GAMMA_INF=ETA_INF/CUBIC_INF

def diffusion_extrema(m:int):
    ds=[sp.Rational(x) for x in diffusion_entries(m)]
    return min(ds),max(ds),sp.factor(max(ds)/min(ds))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',type=Path)
    ap.add_argument('--max-m',type=int,default=100)
    args=ap.parse_args()
    assert R_INF+C_INF/sp.Integer(224)>0
    rows=[]
    for m in range(3,args.max_m+1):
        dmin,dmax,ratio=diffusion_extrema(m)
        eta=eta_formula(m); cubic=cubic_formula(m)
        rows.append(dict(m=m,d_min=float(dmin),d_max=float(dmax),diffusion_ratio=float(ratio),
                         m_eta=float(m*eta),minus_m_c=float(-m*cubic),
                         amplitude_ratio=float(-eta/cubic)))
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True)
        with args.out.open('w',newline='') as fh:
            wr=csv.DictWriter(fh,fieldnames=rows[0].keys());wr.writeheader();wr.writerows(rows)
    print('ASYMPTOTICS_PASS')
    print('h_inf',sp.N(HINF,18))
    print('eta_inf',sp.N(ETA_INF,18))
    print('c_inf',sp.N(CUBIC_INF,18))
    print('gamma_inf',sp.N(GAMMA_INF,18))
    print('diffusion m=3',diffusion_extrema(3))
    print('diffusion m=4',diffusion_extrema(4))
if __name__=='__main__': main()
