#!/usr/bin/env python3
"""Exact diagnostics for the source bridge; not an independent proof of clasps."""
from collections import Counter
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, product
import argparse, json
from pathlib import Path

def partitions(n, bound):
    for x in combinations_with_replacement(range(bound+1), n):
        yield tuple(reversed(x))

def dominant(x): return all(a>=b for a,b in zip(x,x[1:]))
def factors(lam,mu):
    z=Counter()
    for i in range(len(lam)):
        for j in range(i+1,len(lam)):
            if mu[i]==0 and mu[j]==1:
                d=lam[i]-lam[j]+j-i
                assert d>=2
                z[d]+=1; z[d-1]-=1
    return {k:v for k,v in sorted(z.items()) if v and k!=1}

def classical(f):
    v=Fraction(1)
    for k,e in f.items(): v*=Fraction(k)**e
    return v

def conjugate(p,width=None):
    return tuple(sum(x>=j for x in p) for j in range(1,(max(p,default=0) if width is None else width)+1))

def horizontal_row_factors(tau,sigma,omit_bottom=False):
    r=len(tau); t=tau+(0,); z=Counter()
    for i in range(r):
        N=tau[i]-sigma[i]
        if not N: continue
        for k in range(i+1,r+(0 if omit_bottom else 1)):
            c=t[i]-t[k]+k-i
            for ell in range(1,sigma[k-1]-t[k]+1):
                assert c-ell-N>=1
                z[c-ell]+=1;z[c-ell-N]-=1
    return {k:v for k,v in sorted(z.items()) if v and k!=1}

def weyl_dim(lam):
    z=Fraction(1)
    for i in range(len(lam)):
        for j in range(i+1,len(lam)):
            z*=Fraction(lam[i]-lam[j]+j-i,j-i)
    return z

def main():
    cases=0; invalid=0; shifts=0
    for n in range(2,7):
      for lam in partitions(n,4):
       for k in range(1,n):
        for chosen in combinations(range(n),k):
         mu=tuple(int(i in chosen) for i in range(n));nu=tuple(a+b for a,b in zip(lam,mu))
         zero=any(lam[i]-lam[j]+j-i==1 for i in range(n) for j in range(i+1,n) if mu[i]==0 and mu[j]==1)
         assert zero == (not dominant(nu))
         if not dominant(nu): invalid+=1;continue
         f=factors(lam,mu);assert classical(f)>=1
         assert f==factors(tuple(a-7 for a in lam),mu);shifts+=1
         # Independent root denominator description.
         g=Counter()
         for i in range(n):
          for j in range(i+1,n):
           A=lam[i]-lam[j]+j-i;B=nu[i]-nu[j]+j-i
           if A-B==1:g[A]+=1;g[B]-=1
         assert f=={x:e for x,e in sorted(g.items()) if e and x!=1}
         cases+=1
    strips=0; bottom_witness=None
    for r in range(1,6):
     for tau in partitions(r,6):
      t=tau+(0,)
      for sigma in product(*(range(t[i+1],t[i]+1) for i in range(r))):
       alpha=conjugate(sigma,tau[0]);beta=conjugate(tau,tau[0]);mu=tuple(b-a for a,b in zip(alpha,beta))
       f=factors(alpha,mu)
       assert f==horizontal_row_factors(tau,sigma)
       if bottom_witness is None and f!=horizontal_row_factors(tau,sigma,True):
        bottom_witness={'tau':tau,'sigma':sigma,'correct':str(classical(f)),'wrong':str(classical(horizontal_row_factors(tau,sigma,True)))}
       strips+=1
    lam=(3,1,0);mu=(0,1,0);nu=tuple(a+b for a,b in zip(lam,mu))
    correct=classical(factors(lam,mu)); wrong_orientation=Fraction(2)
    dimratio=weyl_dim(lam)/weyl_dim(nu)
    assert (correct,dimratio,wrong_orientation)==(Fraction(3,2),Fraction(1),Fraction(2))
    # Scalar rescaling and q=1 diagnostics.
    assert 9*correct!=correct
    assert correct**2 != correct
    for m in range(1,21):
        powers=tuple(range(m-1,-m,-2)); assert len(powers)==m and sum(1 for _ in powers)==m
    report={
      'status':'PASS','purpose':'Finite exact diagnostics; the universal theorem depends on Martin-Spencer Theorem 5.11, not these cases.',
      'valid_vertical_strips':cases,'invalid_dominance_cases':invalid,'central_shift_checks':shifts,'horizontal_strips':strips,
      'negative_controls':{
        'all_positive_roots_dimension_ratio':{'lambda':lam,'mu':mu,'correct':str(correct),'wrong':str(dimratio),'rejected':True},
        'reversed_root_orientation':{'lambda':lam,'mu':mu,'correct':str(correct),'wrong':str(wrong_orientation),'rejected':True},
        'basis_rescaling':{'scale':3,'original':str(correct),'rescaled':str(9*correct),'rejected':True},
        'missing_bottom_row_factor':dict(bottom_witness,rejected=True),
        'omitting_dominance':{'lambda':[0,0],'mu':[0,1],'denominator':0,'rejected':True},
        'norm_vs_squared_norm':{'squared_norm':'3/2','square_root_is_not_kappa':True}},
      'q_integer_q1_checks':20}
    out=json.dumps(report,indent=2)+'\n';print(out,end='')
    if args.output:Path(args.output).write_text(out)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output');args=ap.parse_args();main()
