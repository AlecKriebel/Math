"""Fresh review enumeration, independent of the supplied diagnostic code."""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from math import comb, pi
import cmath, json

def require(x, message):
    if not x: raise RuntimeError(message)

results=[]
for n in range(3,7):
    E=list(combinations(range(n),2)); N=len(E); at={e:i for i,e in enumerate(E)}
    triangle_masks=[sum(1<<at[e] for e in combinations(v,2)) for v in combinations(range(n),3)]
    by_m=Counter(); hist=Counter()
    for g in range(1<<N):
        m=g.bit_count(); d=[sum(bool(g>>i&1) for i,e in enumerate(E) if v in e) for v in range(n)]
        t=sum(g&mask==mask for mask in triangle_masks)
        w=sum(comb(v,2) for v in d)
        x=sum(bool(g>>i&1 and g>>j&1) for i,j in combinations(range(N),2) if not set(E[i])&set(E[j]))
        require(x==comb(m,2)-w,'ordinary disjoint count')
        by_m[m,w]+=1; hist[m,t,x]+=1
    A=N*(n-2); B=A*(4*n-10)
    if n>=4:
        require(B-4*F(A*A,N)==-2*A,'conditional leading cancellation')
        for m in range(N+1):
            den=comb(N,m); mean=sum(F(c*w,den) for (mm,w),c in by_m.items() if mm==m)
            second=sum(F(c*w*w,den) for (mm,w),c in by_m.items() if mm==m)
            h=lambda j:F(comb(m,j) if m>=j else 0,comb(N,j))
            require(second-mean*mean==A*(h(2)-h(4))+B*(h(3)-h(4))+A*A*(h(4)-h(2)**2),'conditional exact variance')
    for p in [F(1,7),F(1,2),F(6,7)]:
        mass=Counter(); xt=F(0); xt2=F(0)
        for (m,t,x),c in hist.items():
            z=c*p**m*(1-p)**(N-m);mass[t]+=z;xt+=z*x;xt2+=z*x*x
        mu=sum(t*z for t,z in mass.items());v=sum(z*(t-mu)**2 for t,z in mass.items())
        require(sum(mass.values())==1 and 0 in mass and 1 in mass,'mass and span witnesses')
        require(mu==comb(n,3)*p**3,'mean')
        cov=comb(n,3)*p**3*(1-p**3)+12*comb(n,4)*p**5*(1-p)
        lin=N*(n-2)**2*p**5*(1-p); rem=3*comb(n,3)*p**4*(1-p)**2+comb(n,3)*p**3*(1-p)**3
        require(v==cov==lin+rem,'two triangle variance forms')
        require(xt2-xt*xt==N*comb(n-2,2)**2*p**3*(1-p)+3*comb(n,4)*p*p*(1-p)**2,'disjoint true variance')
        require(n==3 or v!=comb(n,3)*p**3*(1-p**3)+6*comb(n,4)*p**5*(1-p),'wrong covariance factor detected')
        for q in [1,2,4,6,11,37,101]:
            residues=[sum(z for t,z in mass.items() if t%q==a) for a in range(q)]
            delta=max(abs(q*z-1) for z in residues)
            coeff=sum(float(z)*cmath.exp(2j*pi*(t%q)/q) for t,z in mass.items())
            require(q==1 or abs(coeff)<=float(delta)+1e-12,'Fourier necessity bound')
            require(q!=1 or delta==0,'unit modulus')
        require(all((6*t)%2==0 for t in mass),'labeled substitution obstruction')
        results.append({'n':n,'p':str(p),'exact_variance':str(v),'graph_states':1<<N})
print(json.dumps({'status':'PASS','fresh_independent_exact_cases':results,'total_graphs':sum(1<<comb(n,2) for n in range(3,7)),'scope':'Finite identities and modular coefficient checks only; analytic proof review supplies asymptotic deduction.'},indent=2))
