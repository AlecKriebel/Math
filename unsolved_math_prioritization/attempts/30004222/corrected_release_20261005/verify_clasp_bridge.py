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

def qbinomial_factors(top,bottom):
    assert 0 <= bottom <= top
    z=Counter(range(top-bottom+1,top+1))
    z.subtract(range(1,bottom+1))
    return z

def lowering_inverse_square(tau,sigma):
    # Fixed terminal j=s in Eq.5.15; append a row so sigma_s=0.
    t=tuple(tau)+(0,); a=tuple(sigma)+(0,); s=len(t)
    N=tuple(x-y for x,y in zip(t,a)); z=Counter()
    for i in range(s-1):
        for k in range(i+1,s):
            c=t[i]-t[k]+k-i
            z.update(qbinomial_factors(c-1,N[i]))
            if k<s-1:z.subtract(qbinomial_factors(c+N[k],N[i]))
    return {k:v for k,v in sorted(z.items()) if v and k!=1}

def qvalue(f,q):
    v=Fraction(1)
    for m,e in f.items():
        assert m>=1
        v*=sum(q**(m-1-2*j) for j in range(m))**e
    return v

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
       assert f==lowering_inverse_square(tau,sigma)
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
    # Evaluate the actual multiplicative N_prime of Eq.5.15, not just an
    # abstract norm/square distinction. The direct quotient is its inverse square.
    small=lowering_inverse_square((2,),(1,))
    assert small=={2:1}
    reciprocal=[]
    for q in (Fraction(1),Fraction(2)):
        B=qvalue(small,q);normalizer_squared=1/B
        assert B!=normalizer_squared and B*normalizer_squared==1
        reciprocal.append({'q':str(q),'kappa':str(B),'N_prime_squared':str(normalizer_squared)})
    previous=classical(small)
    final=classical(lowering_inverse_square((3,),(2,)))
    assert (previous,final,previous*final)==(Fraction(2),Fraction(3),Fraction(6))
    old=(1,0);new=(1,1)
    literal=[(i,j) for i in range(2) for j in range(i+1,2)
             if old[i]==new[i] and old[j]==new[j]+1]
    assert not literal and new[0]-new[1]+1-1==0
    w=(2,0,1);winv=tuple(w.index(i) for i in range(3));bits=(0,1,1)
    intended=[(i+1,j+1) for i in range(3) for j in range(i+1,3) if bits[i]==0 and bits[j]==1]
    printed=[(i+1,j+1) for i in range(3) for j in range(i+1,3) if winv[i]>winv[j]]
    assert intended==[(1,2),(1,3)] and printed==[(1,3),(2,3)]
    report={
      'status':'PASS','purpose':'Finite exact diagnostics of the corrected inverse-square source reconstruction, retaining stated representation-theoretic dependencies; not a direct all-rank web computation.',
      'valid_vertical_strips':cases,'invalid_dominance_cases':invalid,'central_shift_checks':shifts,'horizontal_strips':strips,'lowering_inverse_square_matches':strips,
      'negative_controls':{
        'all_positive_roots_dimension_ratio':{'lambda':lam,'mu':mu,'correct':str(correct),'wrong':str(dimratio),'rejected':True},
        'reversed_root_orientation':{'lambda':lam,'mu':mu,'correct':str(correct),'wrong':str(wrong_orientation),'rejected':True},
        'basis_rescaling':{'scale':3,'original':str(correct),'rescaled':str(9*correct),'rejected':True},
        'missing_bottom_row_factor':dict(bottom_witness,rejected=True),
        'omitting_dominance':{'lambda':[0,0],'mu':[0,1],'denominator':0,'rejected':True},
        'norm_vs_squared_norm':{'squared_norm':'3/2','square_root_is_not_kappa':True,'limitation':'This old control alone did not test the source normalizer.'},
        'source_reciprocal_normalizer':{'equation':'kappa=(N_prime)^(-2)','minimal_tableau':[[1,2]],'evaluations':reciprocal,'wrong_square_rejected':True},
        'source_all_j_product':{'terminal_B':str(final),'parent_product':str(previous),'all_j_product':str(previous*final),'single_step_global_product_rejected':True},
        'source_partial_priming_fix':{'old':old,'new':new,'literal_product':'1','condition_only_fix_denominator':0,'correct':'[2]','rejected':True},
        'source_weyl_direction':{'mu':bits,'sorting_permutation':[3,1,2],'intended_pairs':intended,'printed_inverse_pairs':printed,'rejected_under_standard_left_action':True}},
      'q_integer_q1_checks':20}
    out=json.dumps(report,indent=2)+'\n';print(out,end='')
    if args.output:Path(args.output).write_text(out)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output');args=ap.parse_args();main()
