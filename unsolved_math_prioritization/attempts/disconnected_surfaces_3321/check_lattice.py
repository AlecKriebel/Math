"""Finite checks accompanying an analytic, unbounded proof in FIVE_APPROACHES.md."""
import itertools,json
u,v=(1,2),(2,-1)
X=[u,u,v]
def det(x,y): return x[0]*y[1]-x[1]*y[0]
def f(row): return sum(abs(row[0]*x+row[1]*y) for x,y in X)
L=sum(abs(det(x,y)) for x in X for y in X)
if L!=20: raise RuntimeError("L mismatch")
rows=list(itertools.product(range(-20,21),repeat=2))
nonzero=[r for r in rows if r!=(0,0)]
if min(map(f,nonzero))!=4: raise RuntimeError("minimum row norm mismatch")
if {r for r in nonzero if f(r)==4}!={(1,0),(-1,0)}: raise RuntimeError("equality rows mismatch")
small=[r for r in nonzero if f(r)<=20]
products=[f(r)*f(s) for r in small for s in small if abs(det(r,s))==1]
if min(products)!=20: raise RuntimeError("unimodular minimum mismatch")
print(json.dumps({'L':L,'M_analytic':20,'bounded_unimodular_min':min(products),'proof':'Unbounded lower bound is the congruence argument in FIVE_APPROACHES.md. Enumeration is a consistency check, not the proof.','status':'PASS'},indent=2))
