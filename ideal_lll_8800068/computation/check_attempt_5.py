"""Exact reductions of dual-number evaluation ideals; no inference from sampling."""
import random
import sympy as s
rng=random.Random(880006805)

def check_reduced(B):
    G=[];D=[]
    for i in range(B.rows):
        b=B.row(i);mu=[b.dot(g)/d for g,d in zip(G,D)]
        assert all(abs(x)<=s.Rational(1,2) for x in mu)
        g=b.copy()
        for x,v in zip(mu,G):g-=x*v
        d=g.dot(g)
        if i:assert d+mu[-1]**2*D[-1]>=s.Rational(3,4)*D[-1]
        G.append(g);D.append(d)

for n in (3,5,7,9,13,17):
    r=(n-1)//2;a=r*2**max(3,(n+3)//4);m=a**r+1
    assert s.gcd(r*a,m)==1
    H=s.eye(n);H[0,0]=H[1,1]=m
    for j in range(2,n):
        H[j,0]=((j-1)*a**j+m//2)%m-m//2;H[j,1]=(-j*a**(j-1)+m//2)%m-m//2
    h2=[0]*n;h2[0]=1;h2[r]=2;h2[2*r]=1
    assert sum(h2[j]*a**j for j in range(n))%m==0
    assert sum(j*h2[j]*a**(j-1) for j in range(1,n))%m==0
    cases=[H]
    # Use the first reduced output as a small basis for independent scrambles.
    baseline=H.lll(delta=s.Rational(3,4))
    for _ in range(6):
        U=baseline.copy()
        for __ in range(4*n):
            i,j=rng.sample(range(n),2);c=rng.choice((-2,-1,1,2))
            U[i,:]=U.row(i)+c*U.row(j)
        cases.append(U)
    sq=[];errors=[]
    for B in cases:
        try:
            R=B.lll(delta=s.Rational(3,4));check_reduced(R)
            assert abs(R.det())==m*m
            for row in R.tolist():
                assert sum(row[j]*a**j for j in range(n))%m==0
                assert sum(j*row[j]*a**(j-1) for j in range(1,n))%m==0
            sq.append(int(R.row(0).dot(R.row(0))))
        except Exception as e:errors.append(type(e).__name__)
    print({'n':n,'r':r,'a':a,'m':m,'attempts':len(cases),'successes':len(sq),'errors':errors,'min_first_norm_squared':min(sq) if sq else None,'max_first_norm_squared':max(sq) if sq else None,'lambda1_squared':6},flush=True)
