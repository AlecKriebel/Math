#!/usr/bin/env python3
"""Original audit controls. Standard library only; exact rational arithmetic.
The common pi**(2*n) factor cancels in each assembly probability.
No manuscript-supplied programs or outputs are imported.
"""
from fractions import Fraction as F
from functools import lru_cache
from math import factorial, comb, prod
from pathlib import Path
import datetime, json

OUT=Path(__file__).resolve().parent

def bernoulli(m):
    B=[F(1)]
    for n in range(1,m+1):
        B.append(-sum(F(comb(n+1,k))*B[k] for k in range(n))/F(n+1))
    return B[m]

def abar(j):
    # zeta(2j)/(2j*pi^(2j)); Euler's even-zeta formula.
    return (-1)**(j+1)*bernoulli(2*j)*F(2**(2*j-1),factorial(2*j)*2*j)

@lru_cache(None)
def partitions(n,lower=1):
    if n==0:return ((),)
    return tuple((j,)+rest for j in range(lower,n+1) for rest in partitions(n-j,j))

def histogram(p,n):return tuple(p.count(j) for j in range(1,n+1))
def falling(x,r):return prod(range(x-r+1,x+1)) if x>=r else 0

def mass(c,a):return prod(a[j]**c[j-1]/factorial(c[j-1]) for j in range(1,len(c)+1))

def h_recurrence(n,a):
    h=[F(1)]
    for m in range(1,n+1):h.append(sum(j*a[j]*h[m-j] for j in range(1,m+1))/m)
    return h

def compositions(n):
    if n==0:yield ();return
    for j in range(1,n+1):
        for rest in compositions(n-j):yield (j,)+rest

@lru_cache(None)
def beta_interval(alpha,beta,left,right):
    if beta==0:return F(int(left<=1<=right))
    norm=F(factorial(alpha+beta-1),factorial(alpha-1)*factorial(beta-1))
    return norm*sum(F((-1)**k*comb(beta-1,k),alpha+k)*(right**(alpha+k)-left**(alpha+k)) for k in range(beta))

@lru_cache(None)
def dirichlet_rectangle(alpha1,alpha2,beta,left1,right1,left2,right2):
    assert right1+right2<1
    if beta==0:return F(0) # chosen coordinates sum to one, impossible here
    norm=F(factorial(alpha1+alpha2+beta-1),factorial(alpha1-1)*factorial(alpha2-1)*factorial(beta-1))
    m=beta-1;answer=F(0)
    for k in range(m+1):
        for l in range(m-k+1):
            coefficient=(-1)**(k+l)*comb(m,k)*comb(m-k,l)
            intx=(right1**(alpha1+k)-left1**(alpha1+k))/F(alpha1+k)
            inty=(right2**(alpha2+l)-left2**(alpha2+l))/F(alpha2+l)
            answer+=coefficient*intx*inty
    assert answer>=0
    return norm*answer

def controls():
    N=9;a={j:abar(j) for j in range(1,N+1)};h=h_recurrence(N,a)
    normalization=[];selection_checks=0;mark_checks=0;dirichlet_checks=[]
    W=((F(1,10),F(1,5)),(F(1,4),F(1,3)))
    for n in range(1,N+1):
        states=[(histogram(p,n),mass(histogram(p,n),a)) for p in partitions(n)]
        total=sum(w for c,w in states)
        ordered=sum(prod(a[j] for j in p)/factorial(len(p)) for p in compositions(n))
        assert total==h[n]==ordered
        normalization.append({'n':n,'partitions':len(states),'ordered_compositions':2**(n-1),'h_over_pi_2n':str(h[n])})
        for selected_mass in range(n+1):
            for p in partitions(selected_mass):
                r=histogram(p,n)
                observed=sum(w*prod(falling(c[j],r[j]) for j in range(n)) for c,w in states)/h[n]
                expected=h[n-selected_mass]/h[n]*prod(a[j+1]**r[j] for j in range(n))
                assert observed==expected
                selection_checks+=1
        # Independent Bernoulli marking with size-dependent rational probabilities.
        # Direct product generating polynomials vs selected-component convolution.
        pmark={j:F(j,j+1) for j in range(1,n+1)}
        for order in range(1,4):
            observed=F(0)
            for c,w in states:
                polynomial=[F(1)]
                for j in range(1,n+1):
                    for _ in range(c[j-1]):
                        nxt=[F(0)]*(len(polynomial)+1)
                        for k,v in enumerate(polynomial):
                            nxt[k]+=v*(1-pmark[j]);nxt[k+1]+=v*pmark[j]
                        polynomial=nxt
                observed+=w*sum(v*falling(k,order) for k,v in enumerate(polynomial))/h[n]
            selected=[F(1)]+[F(0)]*n
            for _ in range(order):
                selected=[sum(selected[m-j]*a[j]*pmark[j] for j in range(1,m+1)) for m in range(n+1)]
            expected=sum(selected[m]*h[n-m] for m in range(n+1))/h[n]
            assert observed==expected;mark_checks+=1
        # Exact normalized Dirichlet counts in two separated rational windows.
        if n<=7:
            direct=[F(0),F(0),F(0)];selected=[F(0),F(0),F(0)]
            for c,w in states:
                parts=[j for j in range(1,n+1) for _ in range(c[j-1])]
                first=sum(beta_interval(2*j,2*(n-j),*W[0]) for j in parts)
                pair=F(0);cross=F(0)
                for i,j in enumerate(parts):
                    for ii,k in enumerate(parts):
                        if i==ii:continue
                        pair+=dirichlet_rectangle(2*j,2*k,2*(n-j-k),*W[0],*W[0])
                        cross+=dirichlet_rectangle(2*j,2*k,2*(n-j-k),*W[0],*W[1])
                for t,val in enumerate((first,pair,cross)):direct[t]+=w*val/h[n]
            for j in range(1,n+1):
                selected[0]+=a[j]*h[n-j]/h[n]*beta_interval(2*j,2*(n-j),*W[0])
                for k in range(1,n-j+1):
                    factor=a[j]*a[k]*h[n-j-k]/h[n]
                    selected[1]+=factor*dirichlet_rectangle(2*j,2*k,2*(n-j-k),*W[0],*W[0])
                    selected[2]+=factor*dirichlet_rectangle(2*j,2*k,2*(n-j-k),*W[0],*W[1])
            assert selected==direct
            dirichlet_checks.append({'n':n,'mean_window1':str(direct[0]),'second_factorial_window1':str(direct[1]),'cross_window1_window2':str(direct[2])})
    return {'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_assertions_passed':True,'finite_scope':'n=1..9; normalized Dirichlet n=1..7; two rational windows','exact_selected_component_checks':selection_checks,'exact_Bernoulli_marking_checks':mark_checks,'normalization':normalization,'normalized_Dirichlet_checks':dirichlet_checks}

if __name__=='__main__':
    result=controls();(OUT/'EXACT_CONTROLS_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['normalization','normalized_Dirichlet_checks']},indent=2))
