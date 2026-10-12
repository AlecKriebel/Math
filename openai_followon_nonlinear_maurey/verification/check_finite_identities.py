# Finite error-detection checks; not a proof or formalization.
import random
from fractions import Fraction as F
rng = random.Random(20261006)
phi = lambda r: 3*r*r-2*r*r*r
max_flat=F(0)
checked=0
for bit in (F(0),F(1)):
    for ui in range(11):
        for vi in range(11):
            u=F(ui,10)
            v=F(vi,10)
            a=u-bit
            d=v-u
            R=(v-bit)**4-a**4-4*a**3*d
            lhs=(phi(v)-phi(u))**2
            assert lhs<=108*R, (u,v,bit,lhs,R)
            if R:
                max_flat=max(max_flat,lhs/R)
            checked+=1
recon_checked=0
for _ in range(500):
    n=rng.randrange(1,7)
    k=rng.randrange(1,10)
    x=[[F(rng.randrange(-10,11),rng.randrange(1,6))
        for _ in range(k)] for _ in range(n)]
    v=[min(x[i][a] for i in range(n)) for a in range(k)]
    Bs=[B for B in range(1,2**n-1)]
    b={B:[max(F(0),
        min(x[i][a] for i in range(n) if B>>i&1)
        -max(x[i][a] for i in range(n) if not B>>i&1))
        for a in range(k)] for B in Bs}
    w={B:sum(b[B]) for B in Bs}
    for i in range(n):
        for a in range(k):
            assert v[a]+sum(b[B][a] for B in Bs if B>>i&1)==x[i][a]
        for j in range(n):
            assert sum(abs(x[i][a]-x[j][a]) for a in range(k))==sum(
                w[B] for B in Bs if (B>>i&1)!=(B>>j&1))
    recon_checked+=1
print({'exact_flat_grid_cases':checked,
       'max_ratio_on_grid':str(max_flat),
       'exact_cut_tuples':recon_checked,
       'all_passed':True})
