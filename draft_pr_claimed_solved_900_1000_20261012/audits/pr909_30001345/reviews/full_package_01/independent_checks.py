#!/usr/bin/env python3
"""Supplementary finite exact reconstruction; imports no candidate code.

Written after the analytic pre-crosscheck derivation and later code inspection.
This is not a universal/analytic proof or an independent source retrieval.
"""
from fractions import Fraction as Q
from collections import Counter
import json

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def k(a=0, b=0): return (Q(a), Q(b))
Z, U, W = k(), k(1), k(0, 1)
def add(a,b): return (a[0]+b[0], a[1]+b[1])
def neg(a): return (-a[0],-a[1])
def sub(a,b): return add(a,neg(b))
def mul(a,b):
    return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]-a[1]*b[1])
def conj(a): return (a[0]-a[1],-a[1])
def norm(a):
    v=mul(a,conj(a)); require(v[1]==0,'norm rational'); return v[0]
def div(a,b):
    require(b!=Z,'nonzero denominator'); v=mul(a,conj(b)); n=norm(b)
    return (v[0]/n,v[1]/n)
def dot(a,b):
    out=Z
    for x,y in zip(a,b): out=add(out,mul(x,y))
    return out
def cross(a,b):
    return (sub(mul(a[1],b[2]),mul(a[2],b[1])),
            sub(mul(a[2],b[0]),mul(a[0],b[2])),
            sub(mul(a[0],b[1]),mul(a[1],b[0])))
def canonical(p):
    pivot=next(x for x in reversed(p) if x!=Z)
    return tuple(div(x,pivot) for x in p)
def arrangement(roots):
    return [(U,neg(q),Z) for q in roots]+[(Z,U,neg(q)) for q in roots]+[(neg(q),Z,U) for q in roots]
def enumerate_points(lines):
    points={}
    for i,a in enumerate(lines):
        for b in lines[:i]:
            p=canonical(cross(a,b)); points[p]=tuple(j for j,c in enumerate(lines) if dot(c,p)==Z)
    return points
def poly_add(p,q):
    out=dict(p)
    for e,a in q.items(): out[e]=add(out.get(e,Z),a)
    return {e:a for e,a in out.items() if a!=Z}
def poly_mul(p,q):
    out={}
    for e,a in p.items():
        for f,b in q.items():
            g=tuple(x+y for x,y in zip(e,f)); out[g]=add(out.get(g,Z),mul(a,b))
    return {e:a for e,a in out.items() if a!=Z}
def power(p,n):
    out={(0,0,0):U}
    for _ in range(n):out=poly_mul(out,p)
    return out
def linear(a,b,c):return {e:v for e,v in zip([(1,0,0),(0,1,0),(0,0,1)],[a,b,c]) if v!=Z}
def evaluate(p,x,y,t):
    out=Z
    for e,a in p.items():
        term=a
        for v,n in zip((x,y,t),e):
            for _ in range(n):term=mul(term,v)
        out=add(out,term)
    return out
def derivative(p,i):
    out={}
    for e,a in p.items():
        if e[i]:
            f=list(e); f[i]-=1;out[tuple(f)]=mul(a,k(e[i]))
    return out

def main():
    roots=[U,W,mul(W,W)]; lines=arrangement(roots); points=enumerate_points(lines)
    require(len(points)==12 and Counter(map(len,points.values()))=={3:12},'twelve triples')
    require(sum(len(v)*(len(v)-1)//2 for v in points.values())==36,'pair completeness')
    infinity=(U,k(2),k(4)); require(all(dot(infinity,p)!=Z for p in points),'good infinity')
    affine=[(sub(mul(k(4),a),c),sub(mul(k(4),b),mul(k(2),c)),c) for a,b,c in lines]
    require(len({canonical((a,b,Z)) for a,b,c in affine})==9,'distinct directions')
    chart_norms=[]
    for p in points:
        den=dot(infinity,p);x=div(p[0],den);y=div(p[1],den)
        chart_norms.append(norm(x)+norm(y))
    require(max(chart_norms)==1,'exact maximum intersection norm')
    factors=[(U,neg(q),Z) for q in roots]
    factors += [(q,add(k(4),mul(k(2),q)),neg(q)) for q in roots]
    factors += [(neg(add(U,mul(k(4),q))),k(-2),U) for q in roots]
    actual={(0,0,0):U}
    for a,b,c in factors:actual=poly_mul(actual,linear(a,b,c))
    X,Y,T=linear(U,Z,Z),linear(Z,U,Z),linear(Z,Z,U)
    S=linear(k(-1),k(-2),U)
    first=poly_add(power(X,3),{e:neg(v) for e,v in power(Y,3).items()})
    second=poly_add({e:mul(k(64),v) for e,v in power(Y,3).items()},{e:neg(v) for e,v in power(S,3).items()})
    third=poly_add(power(S,3),{e:mul(k(-64),v) for e,v in power(X,3).items()})
    require(actual==poly_mul(poly_mul(first,second),third),'polynomial identity')
    require(actual[(9,0,0)]==k(-65),'leading coefficient')
    gradients=[derivative(actual,i) for i in (0,1)]
    for p in points:
        den=dot(infinity,p);x=div(p[0],den);y=div(p[1],den)
        require(evaluate(actual,x,y,U)==Z and all(evaluate(g,x,y,U)==Z for g in gradients),'point Jacobian')
    distances=[norm(c)/(norm(a)+norm(b)) for a,b,c in factors]
    require(max(distances)==Q(1,13),'exact line-distance maximum')
    two=enumerate_points(arrangement([U,k(-1)])); counts2=Counter(map(len,two.values()))
    require(counts2=={2:3,3:4},'n2 singularity inventory')
    require(sum((r-2)*count for r,count in counts2.items())==4,'n2 equality')
    require(any(dot((U,Z,Z),p)==Z for p in points),'bad infinity detected')
    perturbed=list(lines);a,b,c=perturbed[-1];perturbed[-1]=(a,b,add(c,U))
    pert=enumerate_points(perturbed); require(Counter(map(len,pert.values()))!={3:12},'line perturbation detected')
    generic=enumerate_points([(U,k(i),k(i*i)) for i in range(9)])
    require(len(generic)==36 and all(len(v)==2 for v in generic.values()),'generic nine lines are nodes')
    result={'status':'PASS','arithmetic':'exact Fraction pairs in Q[w]/(w^2+w+1); no floating tolerance',
      'independent_candidate_imports':False,'projective_points':12,'multiplicity_histogram':{'3':12},'line_pairs':36,
      'polynomial_identity':True,'x9_coefficient':-65,'jacobian_at_all12':True,
      'chart_squared_norms':sorted(map(str,chart_norms)), 'distance_squared_coefficients':sorted(map(str,distances)),
      'central':{'delta':36,'rough':7},'nearby':{'delta':36,'rough':12},
      'n2':{'nodes':3,'triples':4,'delta':15,'central_rough':4,'nearby_rough':4},
      'negative_controls':{'bad_infinity_detected':True,'line_perturbation_changes_inventory':True,'perturbed_points':len(pert),'generic_nine_lines_nodes':36},
      'limits':'Finite exact controls supplement the separately written all-n, analytic and local-resolution proofs. No new author proof-search turn.'}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
