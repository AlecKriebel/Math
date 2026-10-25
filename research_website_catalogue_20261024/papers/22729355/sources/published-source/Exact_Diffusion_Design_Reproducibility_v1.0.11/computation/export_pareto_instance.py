#!/usr/bin/env python3
"""Export exact certified square-root-scaling endpoint instances."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'independent_verifier'))
from pareto_core import reactions, gamma_y, L0, Hlist, Dphys, rcrit, ellref

def sx(x):
    return str(sp.simplify(x))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('m',type=int)
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args(); m=args.m
    L=L0(m); H=Hlist(m,L); D=Dphys(m,L)
    G,Y=gamma_y(m)
    obj={
      'm':m,
      'species':[f'X{i}' for i in range(1,m+1)]+['Z'],
      'reactions':[{'label':q.name,'source':list(q.source),'target':list(q.target)} for q in reactions(m)],
      'pareto_parameter_L':sx(L),
      'equilibrium_inverse_scaling':[sx(x) for x in H],
      'equilibrium':[sx(1/x) for x in H],
      'physical_diffusion':[sx(x) for x in D],
      'right_critical_vector':[sx(x) for x in rcrit(m)],
      'effective_left_vector':[sx(x) for x in ellref(m)],
      'stoichiometric_rank':int(G.rank()),
      'chi_D':sx(max(D)/min(D)),
      'chi_H':sx(max(H)/min(H)),
      'product':sx((max(D)/min(D))*(max(H)/min(H))),
    }
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(obj,indent=2)+'\n')
    print(args.out)
if __name__=='__main__': main()
