"""Exact controls for the shell/packing arithmetic, not a proof of the analytic claims."""
from fractions import Fraction as F
import json
n=0
for q in range(1,9):
    r=F(1,2**q)
    for N in range(1,41):
        mass=(1-r)*sum((r**j for j in range(N)),F(0))
        assert mass==1-r**N
        assert mass<1
        n+=2
for i in range(21):
    a,b=F(1,2**(i+1)),F(1,2**i)
    for j in range(i+1,25):
        c,d=F(1,2**(j+1)),F(1,2**j)
        assert d<=a
        assert b-a==F(1,2**(i+1))
        n+=2
print(json.dumps({'assertions':n,'scope':'finite exact shell and geometric-series arithmetic only'},sort_keys=True))
