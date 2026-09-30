"""Independent exact diagnostics; no simulation or asymptotic theorem certification."""
from fractions import Fraction as Q
from itertools import product
from math import factorial, comb
from pathlib import Path
from hashlib import sha256
import json
counts={}
def check(ok,name):
    assert ok,name
    counts[name]=counts.get(name,0)+1
# Sum independent exact scalar-square mixtures times sign outer products.
# The radial law has E R^2=1 and E R^4=5/2, unlike the submitted verifier.
for d in range(1,4):
    es=list(product((-1,1),repeat=d))
    atoms=[]
    for r2,p in [(Q(1,2),Q(6,7)),(Q(4),Q(1,7))]:
        for e in es:
            atoms.append((p/len(es),tuple(r2*e[i]*e[j] for i in range(d) for j in range(d))))
    for i in range(d*d):
        check(sum(w*a[i] for w,a in atoms)==int(i//d==i%d),'exact isotropy')
    for N in (1,2,3):
        expectation=Q(0)
        for sample in product(atoms,repeat=N):
            weight=Q(1)
            for w,a in sample: weight*=w
            sq=Q(0)
            for i in range(d*d):
                entry=sum(a[i] for w,a in sample)/N-int(i//d==i%d)
                sq+=entry*entry
            expectation+=weight*sq
        check(expectation==Q(5*d*d,2*N)-Q(d,N),'Frobenius variance by full sample enumeration')
# Independent polynomial convolution, without enumerating sign vectors.
for a in product(range(4),repeat=4):
    if not any(a): continue
    norm=sum(x*x for x in a)
    maxk=6
    coeff=[Q(1)]+[Q(0)]*maxk
    for x in a:
        nxt=[Q(0)]*(maxk+1)
        for k in range(maxk+1):
            nxt[k]=sum(coeff[k-j]*Q(x**(2*j),factorial(2*j)) for j in range(k+1))
        coeff=nxt
    for k in range(1,maxk+1):
        check(coeff[k]<=Q(norm**k,2**k*factorial(k)),'Rademacher coefficient domination')
        radial=Q(factorial(2*k),2**k)
        check(radial*factorial(2*k)*coeff[k]<=Q(factorial(2*k)**2*norm**k,4**k*factorial(k)),'exponential radial moments')
# Squared exponential maximum via independent spacings and the survival integral.
for N in range(1,81):
    h=sum((Q(1,j) for j in range(1,N+1)),Q(0))
    variance=sum((Q(1,j*j) for j in range(1,N+1)),Q(0))
    integrated=sum((Q(2*(-1)**(j+1)*comb(N,j),j*j) for j in range(1,N+1)),Q(0))
    check(integrated==h*h+variance,'maximum second moment spacings versus survival')
    check(integrated>=h*h,'maximum Jensen lower bound')
# An alternate fixed unbounded law: R^2=J/2, P(J=j)=2^-j.
# Its mean is one; the truncated moment tends to one by an exact identity.
for m in range(1,61):
    partial=sum((Q(j,2**(j+1)) for j in range(1,m+1)),Q(0))
    check(partial==1-Q(m+2,2**(m+1)),'fixed unbounded radial normalization')
    for N in (m,2*m,4*m):
        cdf=(1-Q(1,2**m))**N
        check(0<cdf<1,'exact maximum CDF')
        check((1-Q(1,2**m))**(N+1)<cdf,'strict maximum escape')
# The exponential-MGF series sum at |t| <= 1/(16 B^2) is bounded by 128 B^4 t^2.
for b2 in (Q(1),Q(3,2),Q(2),Q(5)):
    for denominator in range(16,101):
        t=1/(denominator*b2)
        geometric=(8*b2*t)**2/(1-8*b2*t)
        check(geometric<=128*b2*b2*t*t,'MGF geometric majorant')
    for s in [Q(j,7)*b2 for j in range(1,401)]:
        t=min(s/(256*b2*b2),1/(16*b2))
        check(t*s-128*b2*b2*t*t>=min(s*s/(512*b2*b2),s/(32*b2)),'two Chernoff branches')
# Frobenius exceptional-event square exactly cancels dimension.
for n in range(1,31):
    for r in range(2,12):
        check(Q(n*n,n*r)*Q(1,n)==Q(1,r),'dimension cancellation')
root=Path(__file__).resolve().parent
out={'verdict':'PASS','assertions':sum(counts.values()),'groups':counts,'scope':'Exact independent finite diagnostics supporting the written proof audit; no simulations, no general characterization, and no reproof of the imported Tikhomirov probability theorem.','verifier_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
(root/'independent_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
