"""Independent exact finite controls. Analytic proofs remain necessary."""
from fractions import Fraction as F
from itertools import combinations
from math import prod
import json

checks = 0
cases = 0

def check(p):
    global checks
    assert p
    checks += 1

def det(a):
    a = [list(row) for row in a]
    answer = F(1)
    for j in range(len(a)):
        pivot = next((i for i in range(j, len(a)) if a[i][j]), None)
        if pivot is None:
            return F(0)
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            answer = -answer
        p = a[j][j]
        answer *= p
        for k in range(j + 1, len(a)):
            ratio = a[k][j] / p
            for h in range(j + 1, len(a)):
                a[k][h] -= ratio * a[j][h]
    return answer

def coeff(lam, w, I):
    return prod((w[i] for i in I), start=F(1)) * prod(((lam[j]-lam[i])**2 for i,j in combinations(I,2)), start=F(1))

def add(p, q):
    r = [F(0)] * max(len(p), len(q))
    for i,x in enumerate(p): r[i] += x
    for i,x in enumerate(q): r[i] += x
    return r

spectra = [
    [-2,2], [-5,-4,8], [-5,7,8], [-3,-2,2,3],
    [-1000,-999,-998,-2,7], [-7,-3,-2,0,5,12],
    [F(-2),F(0),F(1,10**8),F(2,10**8),F(4)],
    [F(-3),F(-3)+F(1,10**9),F(1),F(1)+F(1,10**9)+F(1,10**18)],
]
for lam0 in spectra:
    lam = list(map(F,lam0)); n = len(lam)
    raw_weights = [list(map(F,range(1,n+1))), [F(1,10**60)]+[F(i+1) for i in range(n-1)], [F(i+1) for i in range(n-1)]+[F(1,10**60)]]
    for raw in raw_weights:
        w = [x/sum(raw) for x in raw]
        A = [coeff(lam,w,range(n-k,n)) for k in range(n+1)]
        S = [sum(lam[n-k:]) for k in range(n+1)]
        tau0 = [sum((coeff(lam,w,I) for I in combinations(range(n),k)),F(0)) for k in range(n+1)]
        M = [tau0[k]/A[k] for k in range(n+1)]
        zs = [F(1)] if any(x.denominator != 1 for x in lam) else [F(1),F(7,6),F(2)]
        for z in zs:
            cases += 1
            # z = exp(2t); choosing integer eigenvalues makes every value exact.
            exps = [F(1) if z==1 else z**int(x) for x in lam]
            v = [w[i]*exps[i] for i in range(n)]
            moments = [sum((v[i]*lam[i]**j for i in range(n)),F(0)) for j in range(2*n)]
            tau=[]; t1=[]; t2=[]
            for k in range(n+1):
                entries=[]
                for I in combinations(range(n),k):
                    weight = coeff(lam,w,I)*prod((exps[i] for i in I),start=F(1))
                    s=sum((lam[i] for i in I),F(0))
                    entries.append((weight,s))
                tau.append(sum((x for x,s in entries),F(0)))
                t1.append(sum((2*s*x for x,s in entries),F(0)))
                t2.append(sum((4*s*s*x for x,s in entries),F(0)))
                hankel = det([[moments[i+j] for j in range(k)] for i in range(k)])
                check(tau[-1] == hankel)
                e = F(1) if z==1 else z**int(S[k])
                check(A[k]*e <= tau[-1] <= tau0[k]*e)
            log1=[t1[k]/tau[k] for k in range(n+1)]
            log2=[t2[k]/tau[k]-log1[k]**2 for k in range(n+1)]
            a=[(log1[k+1]-log1[k])/2 for k in range(n)]
            da=[(log2[k+1]-log2[k])/2 for k in range(n)]
            b2=[F(0)]+[tau[k-1]*tau[k+1]/tau[k]**2 for k in range(1,n)]+[F(0)]
            check(a[0] == moments[1]/moments[0])
            check(sum(a)==sum(lam))
            check(sum(x*x for x in a)+2*sum(b2)==sum(x*x for x in lam))
            check(sum(F(i+1)*da[i] for i in range(n))==-2*sum(b2))
            for i in range(n):
                check(da[i] == 2*(b2[i+1]-b2[i]))
            for k in range(1,n):
                r=n-k-1; gap=lam[r+1]-lam[r]
                check((log1[k-1]+log1[k+1]-2*log1[k])/2 == a[k]-a[k-1])
                c2=A[k-1]*A[k+1]/A[k]**2
                predicted=gap**2*w[r]/w[r+1]*prod(((lam[j]-lam[r])/(lam[j]-lam[r+1]))**2 for j in range(r+2,n))
                check(c2==predicted)
                e=F(1) if z==1 else z**(-int(gap))
                check(c2*e/M[k]**2 <= b2[k] <= c2*e*M[k-1]*M[k+1])
            # Characteristic polynomial, independent recurrence in the reconstructed a,b^2.
            pprev=[F(1)]; p=[-a[0],F(1)]
            for k in range(1,n):
                q=add([F(0)]+p,[-a[k]*x for x in p])
                q=add(q,[-b2[k]*x for x in pprev])
                pprev,p=p,q
            target=[F(1)]
            for x in lam:
                target=add([F(0)]+target,[-x*y for y in target])
            check(p==target)

# Exact rational boundary/nonmonotonicity and wrong-clock controls.
# n=2, d=4, x0=-3/5 gives b0=8/5, b'(0)=96/25>0.
d=F(4); x=F(-3,5); b=F(8,5)
check(b*b == (d*d/4)*(1-x*x))
check(-d*x*b == F(96,25))
check(-d*x*b != -d*x*b/2)
# With epsilon=b0 the strict first crossing is NOT zero: b initially rises.
# With epsilon=17/10>b0 it IS zero although the maximum d/2 exceeds epsilon.
check(b < F(17,10) < d/2)
# Frozen n=2 early-low example, checked with squared comparisons.
check(F(16*99,10000)<F(1,4)<F(4))
# Frobenius/Gaussian and coefficient constants, n=1 included.
for n in range(1,101):
    q2=F(n*(n*n-1),12)
    check(sum((F(i)-F(n+1,2))**2 for i in range(1,n+1))==q2)
    check(2*n+2*sum(range(1,n))==n*(n+1))
    check(n*(n+1)-2==(n-1)*(n+2))
    check(4*q2*(n-1)*(n+2)==F((n-1)**2*n*(n+1)*(n+2),3))
print(json.dumps({'status':'PASS','exact_predicates':checks,'spectral_samples':cases,'scope':'Independent finite exact Hankel, Toda, spectrum, envelope, normalization, and boundary controls; not all-data proof certificates.'},indent=2))
