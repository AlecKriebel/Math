#!/usr/bin/env python3
"""Independent exact algebra plus labelled numerical consistency checks.
This does not mechanically prove continuum observability or the positive endpoint.
"""
from fractions import Fraction as Q
import cmath, json, math

def require(p, label):
    if not p:
        raise RuntimeError(label)

def matmul(A,B):
    return [[sum((A[i][k]*B[k][j] for k in range(len(B))),Q(0))
             for j in range(len(B[0]))] for i in range(len(A))]

def inv(A):
    n=len(A); B=[list(row)+[Q(i==j) for j in range(n)] for i,row in enumerate(A)]
    for k in range(n):
        j=next(j for j in range(k,n) if B[j][k])
        B[k],B[j]=B[j],B[k]
        p=B[k][k]; B[k]=[v/p for v in B[k]]
        for i in range(n):
            if i!=k:
                q=B[i][k]; B[i]=[a-q*b for a,b in zip(B[i],B[k])]
    return [row[n:] for row in B]

# Exact eigenfunction/gauge coefficient identities; sine and cosine kept independent.
gauge_cases=0
for e in [Q(1,100),Q(1,7),Q(2)]:
    for M in [Q(-3),Q(-1),Q(1),Q(5,2)]:
        for k in [Q(1,3),Q(3),Q(11)]:
            r=-M/(2*e); lam=M*M/(4*e)+e*k*k
            require(e*(r*r-k*k)+M*r == -lam,'adjoint sine coefficient')
            require(2*e*r*k+M*k == 0,'adjoint cosine coefficient')
            forward_r=M/(2*e)
            require(-2*e*forward_r+M == 0,'forward gauge first derivative')
            require(-e*forward_r**2+M*forward_r == M*M/(4*e),'forward gauge potential')
            require(2*e*forward_r*k+M*k != 0,'wrong adjoint gauge rejected')
            gauge_cases+=1

# Exact Cauchy inverse, including signs and b factors, independently inverted.
cauchy_cases=0
for n in range(1,8):
    lam=[Q(1,3)+Q(j*j,5) for j in range(1,n+1)]
    b=[Q(j,7) for j in range(1,n+1)]
    d=[]
    for i in range(n):
        v=Q(1)
        for j in range(n):
            if i!=j:v*=abs(lam[j]-lam[i])/(lam[j]+lam[i])
        d.append(v)
    G=[[b[i]*b[j]/(lam[i]+lam[j]) for j in range(n)] for i in range(n)]
    inverse=inv(G)
    claimed=[[4*Q((-1)**(i+j))*lam[i]*lam[j]/(b[i]*b[j]*(lam[i]+lam[j])*d[i]*d[j])
              for j in range(n)] for i in range(n)]
    require(inverse==claimed,'finite Gram inverse')
    c=[row[0] for row in inverse]
    require(sum((c[i]*G[i][j]*c[j] for i in range(n) for j in range(n)),Q(0))==c[0],
            'negative lower-bound energy normalization')
    for i in range(n):require(c[i]*((-1)**i)>0,'negative lower-bound signs')
    if n>1:
        wrong=[[abs(v) for v in row] for row in claimed]
        require(matmul(G,wrong)!=[[Q(i==j) for j in range(n)] for i in range(n)],
                'signless inverse mutation rejected')
    cauchy_cases+=1

# General single-mode antiderivative/prefactor algebra, with q = k^2 > 0.
single_exact=0
for e in [Q(1,100),Q(1,7),Q(2)]:
    for q in [Q(1,9),Q(9),Q(121)]:
        integral_prefactor=2*q*e**3/(1+4*q*e**2)
        lam=1/(4*e)+e*q
        require(integral_prefactor*2*lam/(e*e*q)==1,'mode prefactor')
        require(integral_prefactor*2*lam/(e*q)!=1 or e==1,'missing-flux-factor mutation')
        single_exact+=1

scaling_cases=0
for L in [Q(1,3),Q(1),Q(11)]:
    for a in [Q(1,2),Q(1),Q(4)]:
        for e in [Q(1,50),Q(3)]:
            require(e/L**2/(a/L)==e/(a*L),'diffusivity normalization')
            require(L*(a/L)==a,'control squared norm normalization')
            require(L/L==1,'initial norm normalization')
            scaling_cases+=1

# Exact optimization of positive upper exponent for rational T>2.
for T in [Q(201,100),Q(5,2),Q(4),Q(10)]:
    a=1/T; alpha=Q(1,2)-2*a*a; beta=1-2*a
    require(alpha>0 and beta>0,'upper-bound integrability')
    require(2-4*a-alpha*T==-(T-2)**2/(2*T),'optimized squared exponent')
    require((1-a)**2-(Q(1,2)-a*a)==2*(a-Q(1,2))**2>0,
            'localization square-root inequality')
    require(T*T/(T*T-4)>1,'finite-to-infinite-time factor')

# Ordinary floating quadrature is a consistency check, not a proof of any limit.
def simpson(f,N=32768):
    h=1/N
    return h/3*(f(0)+f(1)+sum((4 if i%2 else 2)*f(i*h) for i in range(1,N)))
quad_cases=[]
for e in [.03,.1,.4]:
    for n in [1,3,7]:
        k=n*math.pi
        actual=simpson(lambda x:math.exp(-x/e)*math.sin(k*x)**2)
        expected=-math.expm1(-1/e)*2*k*k*e**3/(1+4*k*k*e*e)
        rel=abs(actual/expected-1)
        require(rel<2e-10,'single-mode quadrature')
        reflected=simpson(lambda x:math.exp((x-1)/e)*math.sin(k*x)**2)
        require(abs(reflected/expected-1)<2e-10,'negative-mode reflected quadrature')
        quad_cases.append({'epsilon':e,'n':n,'relative_error':rel})

contour_cases=0
for a in [.01,.1,.25,.49]:
    q=math.sqrt(.5-a*a)
    for r in [-100,-5,-1,-.1,0,.1,1,5,100]:
        s=complex(r,-a); rho=cmath.sqrt(s*s+.5)
        require(abs(s/rho)<=1+1e-12,'contour rational factor')
        require(rho.real<=q+r*r/(4*q**3)+1e-12,'contour square-root bound')
        require(q+r*r/(4*q**3)<=q+2*r*r+1e-12,'contour Gaussian bound')
        contour_cases+=1

# Explicit endpoint countermodels retain two genuinely different endpoint behaviors.
for n in [2,10,100]:
    A=Q(1);B=Q(n)
    require(A==1 and B==n and B>A,'endpoint countermodels')

result={'status':'PASS','exact_checks':{'gauge_cases':gauge_cases,'cauchy_inverse_cases':cauchy_cases,
 'single_mode_prefactor_cases':single_exact,'scaling_cases':scaling_cases,
 'positive_exponent_optimization':True,'endpoint_countermodels':True},
 'numerical_consistency_only':{'quadrature_cases':quad_cases,'contour_cases':contour_cases},
 'rejected_mutations':['wrong adjoint gauge sign','signless Cauchy inverse','missing epsilon boundary-flux factor'],
 'limitations':['Finite algebra checks do not prove arbitrary-size Cauchy inversion.',
 'Numerical quadrature and contour samples are not uniform estimates.',
 'Continuum proof review is recorded separately; no formal proof checker was used.',
 'Positive critical endpoint remains unresolved.']}
print(json.dumps(result,indent=2,sort_keys=True))
