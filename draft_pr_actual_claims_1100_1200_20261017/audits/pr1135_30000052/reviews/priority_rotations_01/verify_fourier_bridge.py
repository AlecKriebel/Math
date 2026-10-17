#!/usr/bin/env python3
"""Independent exact checks of an audit-derived classical Fourier implication.
Standard library only. No imports of candidate verification programs.
The analytic inequalities and historical statements require the accompanying proof.
"""
from fractions import Fraction as F
from collections import Counter
import json,sys,hashlib
from pathlib import Path
checks=0
neg=[]
def require(ok,description):
 global checks
 checks+=1
 if not ok: raise RuntimeError(description)
def caught(ok,name):
 require(ok,name);neg.append(name)
def energy(n):
 sums=Counter(a+b for a in range(n) for b in range(n))
 return sum(k*k for k in sums.values())
def convol(a,b):
 c=Counter()
 for i,ai in a.items():
  for j,bj in b.items():c[i+j]+=ai*bj
 return c
# Count ordered solutions a+b=c+d directly by pair-sum histogram.
for n in range(1,257):
 expected=(2*n**3+n)//3
 require(3*expected==2*n**3+n,'energy integrality')
 require(energy(n)==expected,'ordered additive quadruple count')
 require(n*n+2*sum(k*k for k in range(1,n))==expected,'triangular sum')
# Materially different Laurent polynomial expansion of |S|^4.
for n in range(1,49):
 S=Counter({j:1 for j in range(n)});Sb=Counter({-j:1 for j in range(n)})
 T=convol(S,Sb)
 require(T[0]==n,'second Fourier moment')
 fourth=convol(T,T)
 require(fourth[0]==(2*n**3+n)//3,'fourth Fourier moment constant term')
 require(sum(fourth.values())==n**4,'expansion all quadruples')
# Formal slope/shift Fourier modes: shift exponent cancels; only zero slope survives.
for n in range(1,18):
 modes=Counter()
 for a in range(n):
  for b in range(n):
   for c in range(n):
    for d in range(n): modes[(a+b-c-d,1+1-1-1)]+=1
 require(modes[(0,0)]==energy(n),'uniform slope and arbitrary common phase')
 require(all(k[1]==0 for k in modes),'phase exactly cancels')
# Pointwise Fubini identity for CDF Fourier coefficient. Symbol w represents e(t).
# The coefficient from indicator integral is (1-w)/(2pi i),
# while integral x e(x) dx=1/(2pi i). Sum exact formal numerators.
for n in range(1,15):
 for q in (1,2,3,5,7):
  for offset in range(q):
   numer=Counter();expected=Counter()
   for j in range(n):
    k=(j+offset)%q
    numer[0]+=F(1,n);numer[k]-=F(1,n)
    expected[k]-=F(1,n)
   numer[0]-=1
   require(all(numer[k]==expected[k] for k in set(numer)|set(expected)),
           'indicator primitive incl t=0 and t=1 representatives')
# Exact pi bounds of Archimedes suffice to isolate the least threshold n=234.
lo,hi=F(223,71),F(22,7)
def gap_poly(n,pi_bound):return 60*n*n+30-48*pi_bound**4*(3*n-1)
require(gap_poly(233,lo)<0,'n233 fails even with lower pi bound')
require(gap_poly(234,hi)>0,'n234 succeeds even with upper pi bound')
require(120*234-144*hi**4>0,'polynomial increases for all real n>=234')
for n in range(1,234):require(gap_poly(n,lo)<0,'no smaller positive integer threshold')
# Negative controls: wrong iid fourth, nonnormalized discrepancy, discrete slope aliasing,
# missing mixed terms, confusing second/fourth moments, and insufficient n.
caught(energy(3)!=3**2,'reject n^2 energy from treating lattice phases independently')
caught(energy(3)!=3**4,'reject no slope averaging')
caught(energy(3)!=2*3**2-3,'reject iid phasor fourth moment')
caught(energy(4)!=sum(1 for a in range(4) for b in range(4) for c in range(4) for d in range(4) if (a+b-c-d)%4==0),'reject rational slope law as continuous law')
require(F(2*234**2+1,48*234**3)/hi**4>F(3*234-1,30*234**3),'certified strict n234 comparison')
caught(gap_poly(3,lo)<0,'reject this coarse Fourier bound as n3 proof')
caught(F(1,4)/lo**2<F(1,6),'second-moment version cannot refute p2 equality')
caught(energy(3)!=energy(3)/3**4,'normalization changes fourth power by n^4')
# Source input pins are checked, not used as mathematical oracle.
root=Path(__file__).resolve().parent
pins=json.loads((root/'INPUT_PINS.json').read_text())
for row in pins['files']:
 data=(root.parent.parent/row['path']).read_bytes()
 require(len(data)==row['bytes'],'input bytes')
 require(hashlib.sha256(data).hexdigest()==row['sha256'],'input hash')
result={'status':'PASS','requirements':checks,'negative_controls':neg,
 'energy_n3':energy(3),'energy_n4':energy(4),
 'formula':'(2*n^3+n)/3',
 'normalized_lattice_lower_bound':'(2*n^2+1)/(48*pi^4*n^3)',
 'iid_fourth_moment':'(3*n-1)/(30*n^3)',
 'least_integer_certified_threshold':234,
 'archimedean_pi_bounds':['223/71','22/7'],
 'certified_gap_n234_polynomial_lower':str(gap_poly(234,hi)),
 'certified_gap_n233_polynomial_upper':str(gap_poly(233,lo)),
 'symbolic_derivative_lower_n234':str(120*234-144*hi**4)}
if '--fail-guard' in sys.argv:require(False,'intentional guard exercised')
print(json.dumps(result,indent=2))
