"""Exact sparse operator polynomials, without Hilbert-space compression or writes."""
from fractions import Fraction as Q
from math import comb
import json

def need(ok,message):
    if not ok: raise RuntimeError(message)

def plus(*vectors):
    ans={}
    for v in vectors:
        for k,c in v.items():ans[k]=ans.get(k,Q(0))+c
    return {k:c for k,c in ans.items() if c}

def scale(c,v):return {k:c*a for k,a in v.items() if c*a}

def V(v):return {(j+1,2*k):c for (j,k),c in v.items()}

def Vs(v):return {(j-1,k//2):c for (j,k),c in v.items() if k%2==0}

def D(v):return {(j+1,k):c for (j,k),c in v.items()}

def X(v,eps):
    return plus(scale(eps,V(v)),scale(eps,Vs(v)),scale(eps*eps,V(Vs(v))))

def inverse_root_atom(index,eps,N):
    term=plus({index:Q(1)},scale(eps,V({index:Q(1)})))
    ans={}
    for n in range(N+1):
        cn=Q((-1)**n*comb(2*n,n),4**n)
        ans=plus(ans,scale(cn,term))
        term=X(term,eps)
    return ans

def serial(q):return str(q)

def main():
    eps=Q(1,100);q=2*eps+eps*eps;N=12
    count=0
    for j in range(-4,5):
        for k in range(-5,6):
            e={(j,k):Q(1)}
            need(Vs(V(e))==e,'V*V=I')
            need(D(V(e))==V(D(e)),'dilation commutation')
            need(D(Vs(e))==Vs(D(e)),'adjoint dilation commutation')
            count+=1
    h={(0,0):Q(1)};th={(0,1):Q(1)}
    need(Vs(h)=={(-1,0):1} and not Vs(th),'even/odd boundary')
    # AA* and A*A differ at the unilateral root; this catches the order error.
    root_X=X(th,eps)
    wrong_X=plus(scale(eps,V(th)),scale(eps,Vs(th)),scale(eps*eps,th))
    need(plus(wrong_X,scale(-1,root_X))==scale(eps*eps,th),'frame/Gram order control')
    uh=inverse_root_atom((0,0),eps,N)
    uth=inverse_root_atom((0,1),eps,N)
    need(all(k==0 for j,k in uh),'bilateral chain support')
    need(all(j>=0 and k==2**j for j,k in uth),'unilateral chain support')
    # g=T e(-1,0): g is orthogonal to the entire Th chain, whereas T^-1g=e(-1,0).
    scalar=-uh.get((-1,0),Q(0))
    tail=Q(comb(2*(N+1),N+1),4**(N+1))*(1+eps)*q**(N+1)/(1-q)
    lower,upper=scalar-tail,scalar+tail
    need(lower>Q(4999,1000000) and upper<Q(5001,1000000),'certified scalar interval')
    need(lower>Q(1,1000),'actual inverse-root defect lower bound')
    original_R=q*q/(1-q)
    original_RB=original_R+eps*eps/2
    original_E=eps*eps+(1+eps)*original_RB
    need(original_E<20*eps*eps,'original remainder')
    sharper=Q(3,2)*eps*eps+eps**3/2+Q(3,8)*(1+eps)*q*q/(1-q)
    need(sharper<Q(31,10)*eps*eps,'independent sharper remainder')
    need(eps/2-2*sharper>Q(219,50000),'independent norm defect bound')
    # Zero perturbation must have zero defect; the theorem is not claimed at eps=0.
    need(inverse_root_atom((0,0),Q(0),N)==h,'epsilon-zero control')
    return {'epsilon':str(eps),'polynomial_degree':N,'basis_controls':count,
            'scalar_polynomial':serial(scalar),'tail_bound':serial(tail),
            'certified_scalar_interval':[serial(lower),serial(upper)],
            'interval_decimal_for_orientation_only':[float(lower),float(upper)],
            'original_E_bound':serial(original_E),'sharper_E_bound':serial(sharper),
            'strict_simple_norm_defect_lower_bound':'219/50000',
            'scope':'Exact full-operator polynomials plus analytic norm tail; no compressed matrix/eigenvalue approximation.'}

if __name__=='__main__':print(json.dumps(main(),indent=2,sort_keys=True))
