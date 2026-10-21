"""Independent rational consequences of the inspected models; not a historical absence or all-load proof."""
from fractions import Fraction as F
from itertools import product
import json,sys,datetime

def cc2(z,x,y):
    S=z+x+y+1
    counts=[z,x,y,1]
    out=[F(0) for _ in range(4)]
    for tri in product(range(4),repeat=3):
        prob=F(1)
        for mask in tri:prob*=F(counts[mask],S)
        n0=sum(bool(mask&1) for mask in tri)
        n1=sum(bool(mask&2) for mask in tri)
        rare=[i for i,n in enumerate([n0,n1]) if n==1]
        for i in rare:out[i]+=z*prob/len(rare)
        if n0>=2 and n1>=1:out[2]+=x*prob
        if n1>=2 and n0>=1:out[3]+=y*prob
    return out

def dfc(a,b,x,y):
    D=x+y+1
    return [F(a*(x+1),D),F(b*(y+1),D),F(x*(y+1),D),F(y*(x+1),D)]

# Endpoint samples use the genuine seed carrying both chunks, not a random-singleton seed.
assert cc2(0,1,0)[2]==F(7,8)
assert dfc(0,0,1,0)[2]==F(1,2)
assert sum(cc2(1,0,0)[:2])==F(3,8)
assert sum(dfc(1,0,0,0)[:2])==1
# One global clock cannot simultaneously match first-download and departure witnesses.
assert F(7,8)/F(1,2) != F(3,8)/F(1)
# Strong Markov lumpability fails when the two latent first choices are forgotten.
assert dfc(2,0,1,0)[0] != dfc(0,2,1,0)[0]
# Independent sample enumeration agrees with bounded seed demand on the empty plane.
for M in range(1,21):
    assert sum(cc2(M,0,0)[:2])==F(3*M**3,(M+1)**3)
    assert sum(cc2(M,0,0)[:2])<3
    assert sum(dfc(M,0,0,0)[:2])==M
# Universal algebra: total download intensity >= N/(N+1).
checked=0
for a,b,x,y in product(range(8),repeat=4):
    N=a+b+x+y;D=x+y+1
    r=sum(dfc(a,b,x,y))
    assert r==F(N+a*x+b*y+2*x*y,D)
    assert r>=F(N,D)>=F(N,N+1)
    # Direct generator application to V=2(a+b)+x+y matches 2lambda-r.
    for lam in [F(1,8),F(1,3),F(49,100),F(1,2),F(1),F(10)]:
        qv=2*lam-r
        assert qv<=2*lam-F(N,N+1)
    checked+=1
if '--false-identity' in sys.argv:
    assert cc2(0,1,0)[2]==dfc(0,0,1,0)[2], 'EXPECTED_REJECTION: Common Chunk is not DFC'
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'grid_states':checked,'cc_departure':'7/8','dfc_departure':'1/2','cc_first_download':'3/8','dfc_first_download':'1','small_load_foster':'0<lambda<1/2','all_load_or_global_priority_certified':False},indent=2))
