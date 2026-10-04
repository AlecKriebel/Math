#!/usr/bin/env python3
"""Finite exact algebra controls; the analytic arguments remain written proofs."""
from fractions import Fraction as Q
from math import comb
import argparse,json,sys

checks=[]
def test(name,condition):
 if not condition:raise AssertionError(name)
 checks.append(name)
def choose(a,n):
 out=Q(1)
 for k in range(n):out*=Q(a-k,k+1)
 return out
def rise(b,n):return (-1)**n*choose(-b,n)
def clean(p):return {ij:c for ij,c in p.items() if c}
def add(p,q,scale=Q(1)):
 r=dict(p)
 for ij,c in q.items():r[ij]=r.get(ij,Q(0))+scale*c
 return clean(r)
def deriv(p,var):
 r={}
 for (i,j),c in p.items():
  k=(i,j)[var]
  if k:r[(i-(var==0),j-(var==1))]=c*k
 return clean(r)
def shift(p,var):return {(i+(var==0),j+(var==1)):c for (i,j),c in p.items()}
def scale(p,t):return clean({ij:c*t for ij,c in p.items()})
def lift(a,al,be):
 return clean({(k,n-k):a[n]*choose(al,k)*rise(be,n-k) for n in range(len(a)) for k in range(n+1)})
def diagonal(p):
 r={}
 for (i,j),c in p.items():r[i+j]=r.get(i+j,Q(0))+(-1)**i*c
 return {i:c for i,c in r.items() if c}
def val_univariate(p,x):return sum(c*x**n for n,c in enumerate(p))
def run():
 als=[Q(1),Q(11,10),Q(3,2),Q(7,3),Q(5)]
 bes=[Q(1),Q(5,3),Q(3)]
 for al in als:
  for n in range(25):test(f'binomial lowering alpha={al}, n={n}',choose(al-1,n)==(1-Q(n)/al)*choose(al,n))
  for be in bes:
   a=[Q((-1)**n,n+1) for n in range(13)]
   f=lift(a,al,be);g=lift(a,al-1,be);fu=deriv(f,0);fv=deriv(f,1);fuv=deriv(fu,1)
   test(f'lowering polynomial alpha={al}, beta={be}',g==add(f,shift(fu,0),-1/al))
   test(f'EPD alpha={al}, beta={be}',add(shift(fuv,0),shift(fuv,1))==add(scale(fv,al),scale(fu,-be)))
   want={n:a[n]*(-1)**n*choose(al-be,n) for n in range(len(a))}
   want={n:c for n,c in want.items() if c}
   test(f'diagonal identity alpha={al}, beta={be}',diagonal(f)==want)
   if al.denominator==1:test(f'integer u-degree alpha={al}, beta={be}',all(i<=al for i,j in f))
 for al in [Q(11,10),Q(3,2),Q(7,3),Q(5)]:
  N=int(2*al)+1;u=al/(N-al);p=[Q(comb(N,n)) for n in range(N+1)];lp=[(1-Q(n)/al)*p[n] for n in range(N+1)]
  test(f'generic barrier interior alpha={al}',0<u<1)
  test(f'generic barrier vanishes alpha={al}',val_univariate(lp,u)==0)
  test(f'generic barrier original nonzero alpha={al}',val_univariate(p,u)>0)
 # Exact real-part root identity for Gaussian-rational points, written using pairs.
 for ur,ui in [(Q(0),Q(0)),(Q(1,2),Q(1,3)),(Q(-3,4),Q(1,5))]:
  for zr,zi in [(Q(1),Q(0)),(Q(0),Q(-1)),(Q(3,2),Q(1,4))]:
   d=(ur-zr)**2+(ui-zi)**2
   real=(ur*(ur-zr)+ui*(ui-zi))/d
   rhs=(zr*zr+zi*zi-ur*ur-ui*ui)/(2*d)
   test(f'root half-plane identity {ur,ui,zr,zi}',Q(1,2)-real==rhs and rhs>0)
 # Coefficients of ((1+u)^3+(1-u)^3)/2.
 avg=[Q(comb(3,n)*(1+(-1)**n),2) for n in range(4)]
 test('normalized zero-free averaging obstruction',avg==[1,0,3,0])
 test('averaging obstruction root squared',Q(1)+3*Q(-1,3)==0)
 # Check necessary measure moments leave any fixed total-variation bound.
 for al in [Q(11,10),Q(3,2),Q(7,3)]:
  for B in [1,10,100]:
   n=int(al*(B+2))+1
   test(f'moment obstruction alpha={al}, bound={B}',abs(1-Q(n)/al)>B)
 return {'result':'PASS','exact_checks':len(checks),'checks':checks,'python':sys.version.split()[0],
 'scope':'Finite exact rational algebra controls, not verification of the analytic argument-principle, convergence, Rouche or literature claims. No finite test proves Problem 5.60.'}
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--output');args=parser.parse_args();r=run();s=json.dumps(r,indent=2)+'\n'
 if args.output:open(args.output,'w').write(s)
 print(json.dumps({k:r[k] for k in ['result','exact_checks','scope']}))
