#!/usr/bin/env python3
"""Bounded, heuristic root-radius search. It does not certify zero-freeness."""
import argparse, json, math, random, platform
import numpy as np
from fractions import Fraction

def binom(a,n):
 q=Fraction(1)
 for k in range(n):q*= (a-k)/(k+1)
 return q

def coefficients(alpha,beta,N,x):
 b=[binom(alpha,k) for k in range(N+1)]
 d=[(-1)**k*binom(-beta,k) for k in range(N+1)]
 return np.array([sum(float(b[k]*d[n-k])*x**k for k in range(n+1)) for n in range(N+1)])

def radius(a,kernels):
 vals=[]
 for c in kernels:
  roots=np.roots((np.array(a)*c)[::-1]); vals.append(min(abs(roots)))
 j=int(np.argmin(vals)); return float(vals[j]),j

def run():
 seed=2305060;rng=random.Random(seed);grid=96;trials=24
 params=[(Fraction(a),Fraction(b)) for a in ['11/10','5/4','3/2','7/4','9/4'] for b in ['1','3/2','3']]
 degrees=[3,4,6,8]; records=[];best=None;total=0
 for alpha,beta in params:
  for N in degrees:
   if N<=2*alpha:continue
   xs=np.exp(2j*np.pi*np.arange(grid)/grid)
   k0=[coefficients(alpha,beta,N,x) for x in xs]
   k1=[coefficients(alpha-1,beta,N,x) for x in xs]
   best_local=None
   for t in range(trials):
    raw=[(1,0)]+[(rng.randint(-12,12),rng.randint(-12,12)) for _ in range(N)]
    if raw[-1]==(0,0):raw[-1]=(1,0)
    a=[complex(p,q) for p,q in raw]
    r0,j0=radius(a,k0);r1,j1=radius(a,k1);ratio=r1/r0
    row={'alpha':str(alpha),'beta':str(beta),'degree':N,'trial':t,'radius_premise_grid':r0,'radius_conclusion_grid':r1,'ratio':ratio,'phase_index_premise':j0,'phase_index_conclusion':j1,'coefficients':raw}
    if best_local is None or ratio<best_local['ratio']:best_local=row
    if best is None or ratio<best['ratio']:best=row
    total+=1
   records.append(best_local)
 # Denser control of the ten most promising examples.
 refined=[]
 for row in sorted(records,key=lambda r:r['ratio'])[:10]:
  a=[complex(p,q) for p,q in row['coefficients']];al=Fraction(row['alpha']);be=Fraction(row['beta']);N=row['degree'];g=4096
  xs=np.exp(2j*np.pi*np.arange(g)/g)
  r0,j0=radius(a,[coefficients(al,be,N,x) for x in xs]);r1,j1=radius(a,[coefficients(al-1,be,N,x) for x in xs])
  refined.append({**row,'refinement_grid':g,'refined_premise_radius':r0,'refined_conclusion_radius':r1,'refined_ratio':r1/r0})
 return {'method':'Floating-point roots sampled at equally spaced x on the unit circle; no proof or interval certification. A ratio below 1 would only nominate a candidate.','seed':seed,'initial_grid':grid,'trials_per_parameter_degree':trials,'sample_count':total,'numpy':np.__version__,'python':platform.python_version(),'minimum_grid_ratio':best['ratio'],'ratios_below_one':sum(r['ratio']<1 for r in records),'best_per_parameter_degree':records,'refined_best':refined,'limits':'No angles between samples certified; no analytic-function claim; random search covers no complete coefficient set.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',default='SEARCH.json');a=p.parse_args();r=run();open(a.output,'w').write(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['sample_count','minimum_grid_ratio','ratios_below_one','numpy','python']}));print('minimum refined ratio',min(x['refined_ratio'] for x in r['refined_best']))
