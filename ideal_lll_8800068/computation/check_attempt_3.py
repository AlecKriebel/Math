"""Exact exploratory reductions of evaluation-kernel ideals with planted shortest vector."""
import random
import sympy as s
rng=random.Random(880006803)

def reduced(B):
    G=[]; D=[]
    for i in range(B.rows):
        r=B.row(i)
        mu=[r.dot(g)/d for g,d in zip(G,D)]
        assert all(abs(u)<=s.Rational(1,2) for u in mu)
        g=r-s.zeros(1,B.cols)
        for u,v in zip(mu,G):g-=u*v
        d=g.dot(g)
        if i:assert d+mu[-1]**2*D[-1]>=s.Rational(3,4)*D[-1]
        G.append(g);D.append(d)

for n in (2,3,4,6,8,10,12,16):
    a=2**((n+3)//4); m=a**(n-1)+1
    H=s.eye(n);H[0,0]=m
    for i in range(1,n):H[i,0]=-pow(a,i,m)
    N=s.zeros(n)
    for i in range(n-1):N[i,i]=a;N[i,i+1]=-1
    N[n-1,0]=N[n-1,n-1]=1
    assert abs(N.det())==m
    for r in N.tolist():assert sum(r[i]*a**i for i in range(n))%m==0
    cases=[H,N]
    for trial in range(12):
        U=N.copy()
        for _ in range(5*n):
            i,j=rng.sample(range(n),2);c=rng.choice((-3,-2,-1,1,2,3))
            U[i,:]=U.row(i)+c*U.row(j)
        cases.append(U)
    sq=[];errors=[]
    for B in cases:
        try:
            R=B.lll(delta=s.Rational(3,4)); reduced(R)
            # Membership and determinant certify that this remains the exact ideal.
            assert abs(R.det())==m
            assert all(sum(r[i]*a**i for i in range(n))%m==0 for r in R.tolist())
            sq.append(int(R.row(0).dot(R.row(0))))
        except Exception as e:errors.append(type(e).__name__)
    print({'n':n,'a':a,'m':m,'attempts':len(cases),'successes':len(sq),'errors':errors,'min_first_norm_squared':min(sq) if sq else None,'max_first_norm_squared':max(sq) if sq else None,'lambda1_squared':2},flush=True)
