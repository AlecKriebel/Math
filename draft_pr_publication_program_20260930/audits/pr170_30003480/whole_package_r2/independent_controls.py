"""Independent exact controls for tensor preservation and determinant arithmetic."""
from fractions import Fraction as R
from itertools import product
from math import prod
from random import Random
from pathlib import Path
import json, argparse
ap=argparse.ArgumentParser();ap.add_argument('--mutate',choices=['none','vector_norm','Q2_factor','hull_witness'],default='none');opt=ap.parse_args()
checks={}
def req(ok,name):
    if not ok:raise RuntimeError(name)
    checks[name]=checks.get(name,0)+1
def gram(tensor,mode):
    rest={bits[:mode]+bits[mode+1:] for bits in tensor}
    rows=[[],[]]
    for r in sorted(rest):
        for bit in [0,1]:rows[bit].append(tensor.get(r[:mode]+(bit,)+r[mode:],R(0)))
    a=sum(x*x for x in rows[0]);b=sum(x*x for x in rows[1]);c=sum(x*y for x,y in zip(*rows))
    return (a,c,b)
def norm(t):return sum(x*x for x in t.values())
def det(g):a,c,b=g;return a*b-c*c
rng=Random(17030003480)
for case in range(80):
    tensor={b:R(rng.randrange(-3,4),20) for b in product([0,1],repeat=3)}
    req(0<norm(tensor)<=1,'initial tensor inside ball')
    base_norm=norm(tensor);base_grams=[gram(tensor,i) for i in range(3)]
    for n in range(4,9):
        u=(R(3,5),R(4,5) if opt.mutate!='vector_norm' else R(3,5))
        tensor={bits+(i,):a*u[i] for bits,a in tensor.items() for i in [0,1]}
        req(norm(tensor)==base_norm,'appended unit factor preserves norm')
        req([gram(tensor,i) for i in range(3)]==base_grams,'appended unit factor preserves every retained Gram entry')
        req(all(det(gram(tensor,i))==0 for i in range(3,n)),'all appended flattenings have exact zero determinant')
        # Peel the appended vector using contraction against u, since ||u||=1.
        peeled={b:sum(tensor[b+(i,)]*u[i] for i in [0,1]) for b in product([0,1],repeat=n-1)}
        req(norm(peeled)==base_norm,'unit-factor contraction preserves norm')
        req([gram(peeled,i) for i in range(3)]==base_grams,'unit-factor contraction preserves retained Grams')
roots=[R(49,100),R(36,100),R(36,100),R(1,100)]
d=[r*r for r in roots];slacks=[sum(d)-2*x for x in d]
q1=prod(slacks)
# Pair opposite signs independently. n=4 gives eight opposite pairs, so
# the full 16-sign product is the square of the half-product.
half=prod(roots[0]+sum(sign*x for sign,x in zip(s,roots[1:])) for s in product([-1,1],repeat=3))
q2=(R(1,2) if opt.mutate!='Q2_factor' else R(1))*half*half
req(q2==R(23632249608,2384185791015625),'opposite-sign pairing reproduces exact Q2')
req(q1-q2==R(2589624828909,4768371582031250),'independent positive polynomial difference')
req(min(slacks)>0 and all(0<x<R(1,4) for x in d),'strict positive cube-hull witness')
ts=(R(5,16),R(1,8),R(1,8));ds=[t*(1-t) for t in ts]
req(ts[0]>ts[1]+ts[2] and ds==[R(55,256),R(28,256),R(28,256)],'strict hull infeasible zero-polynomial control')
req(min(sum(ds)-2*x for x in ds)==(R(1,256) if opt.mutate!='hull_witness' else R(0)),'exact hull witness minimum slack')
out=dict(status='PASS',seed=17030003480,checks=checks,total_checks=sum(checks.values()),tensor_cases=80,dimensions=[4,5,6,7,8],unit_vector=['3/5','4/5'],Q2_via_opposite_sign_pairing=str(q2),Q1_minus_Q2=str(q1-q2),hull_slacks=[str(x) for x in slacks],universal_proof_not_inferred_from_controls=True)
print(json.dumps(out,sort_keys=True))
