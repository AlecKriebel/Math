"""Fresh adversarial control using SymPy's exact algebraic-number domain.

This implementation was written after exposure; independent verification,
not independent discovery. No candidate/sibling arithmetic code is imported.
"""
from sympy import Poly,Symbol,cyclotomic_poly
from sympy.polys.domains import QQ
from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations
from collections import Counter
from pathlib import Path
import json

D=Path(__file__).resolve().parent

def run(q):
    n=5*q;x=Symbol('x');poly=Poly(cyclotomic_poly(n,x),x)
    assert poly.is_irreducible
    K=QQ.alg_field_from_poly(poly,alias=f'z{n}')
    zero,one,z=K.zero,K.one,K.unit
    roots=[z**j for j in range(n)]
    assert len(set(roots))==n and z**n==one
    @lru_cache(None)
    def mul(a,b):return a*b
    def cross(a,b):return (mul(a[1],b[2])-mul(a[2],b[1]),mul(a[2],b[0])-mul(a[0],b[2]),mul(a[0],b[1])-mul(a[1],b[0]))
    @lru_cache(None)
    def inverse(a):return one/a
    def normal(v):
        scale=inverse(next(a for a in v if a!=zero))
        return tuple(mul(a,scale) for a in v)
    def dot(a,b):return sum((mul(v,w) for v,w in zip(a,b)),zero)
    full={}
    for family in range(3):
        for j,r in enumerate(roots):
            line=[(one,-r,zero),(zero,one,-r),(-r,zero,one)][family]
            full[normal(line)]=(family,j)
    retained={l:tag for l,tag in full.items() if tag[1]%5 in (0,2,3)}
    vertices={normal(v) for v in [(one,zero,zero),(zero,one,zero),(zero,zero,one)]}
    kind={}
    for i,u in enumerate(roots):
        for j,v in enumerate(roots):
            triple=((i-j)%n,j,(-i)%n)
            hits=[t%5 in (0,2,3) for t in triple]
            if sum(hits)>=2:
                p=normal((u,v,one))
                kind[p]='double' if sum(hits)==2 else ('H' if all(t%5==0 for t in triple) else 'T')
    for p in vertices:kind[p]='vertex'
    points=list(kind)
    actual={normal(cross(a,b)) for a,b in combinations(retained,2)}
    assert actual==set(points)
    assert Counter(kind.values())=={'H':q*q,'double':6*q*q,'T':6*q*q,'vertex':3}
    line_pairs={}
    representative={}
    for i,j in combinations(range(len(points)),2):
        l=normal(cross(points[i],points[j]))
        line_pairs.setdefault(l,set()).update((i,j));representative.setdefault(l,(i,j))
    # Pair-group completeness: every marked third point on a line contributes its own pair.
    comp_support={l:{i for i,p in enumerate(points) if dot(l,p)==zero} for l in retained}
    assert all(line_pairs[l]==I for l,I in comp_support.items())
    for l,I in line_pairs.items():
        if l not in full:assert len(I)<=2
        elif l not in retained:
            assert len(I)==q+1
            assert Counter(kind[points[i]] for i in I)=={'vertex':1,'double':q}
    assert max(map(len,line_pairs.values()))==4*q+1
    olddual={i:Q(1,q) if kind[p]=='H' else Q(1,2*q) if kind[p]=='double' else Q(0) for i,p in enumerate(points)}
    oldload=max(sum(olddual[i] for i in I) for I in line_pairs.values())
    if q==1:
        hi=next(i for i,p in enumerate(points) if kind[p]=='H')
        aux={normal(cross(points[hi],p)) for p in points if kind[p]=='double'}
        assert len(aux)==6 and not aux.intersection(full)
        assert all(len(line_pairs[l])==2 for l in aux)
        primal={l:Q(1,9) if tag[1]%5==0 else Q(4,9) for l,tag in retained.items()}
        primal.update({l:Q(1,9) for l in aux})
        dual={i:{'H':Q(2,3),'double':Q(1,3),'T':Q(1,6),'vertex':Q(0)}[kind[p]] for i,p in enumerate(points)}
        target=Q(11,3)
        assert oldload==Q(3,2)
        # Negative controls deliberately reject the component dual globally and underweight H.
        assert any(sum(olddual[i] for i in I)>1 for I in line_pairs.values())
        broken={l:w for l,w in primal.items() if l not in aux}
        assert sum(w for l,w in broken.items() if hi in line_pairs[l])==Q(1,3)<1
    else:
        primal={l:Q(1,3) if tag[1]%5==0 else Q(1,2) for l,tag in retained.items()}
        dual=olddual;target=Q(4*q)
        assert oldload<=1
    cover=[sum(w for l,w in primal.items() if i in line_pairs[l]) for i in range(len(points))]
    loads=[sum(dual[i] for i in I) for I in line_pairs.values()]
    assert min(cover)>=1 and max(loads)<=1
    assert sum(primal.values())==sum(dual.values())==target
    # Full incidence artifact gives representative pair and complete support per geometric line.
    records=sorted([{'representative_pair':list(representative[l]),'support':sorted(I),'class':'retained' if l in retained else 'deleted' if l in full else 'other','dual_load':str(sum(dual[i] for i in I))} for l,I in line_pairs.items()],key=lambda r:(r['support'],r['representative_pair']))
    (D/'streams'/f'new_q{q}_all_line_incidence.json').write_text(json.dumps({'n':n,'point_kinds':[kind[p] for p in points],'records':records},sort_keys=True))
    result={'q':q,'field_polynomial':str(poly.as_expr()),'field_irreducible':True,'all_coordinate_pair_intersections_match':True,'points':len(points),'components':len(retained),'all_pair_lines':len(line_pairs),'support_histogram':dict(sorted(Counter(map(len,line_pairs.values())).items())),'old_component_dual_global_max_load':str(oldload),'new_primal_cost':str(sum(primal.values())),'new_dual_cost':str(sum(dual.values())),'min_coverage':str(min(cover)),'max_dual_load':str(max(loads)),'negative_controls':'PASS' if q==1 else 'not applicable','status':'PASS'}
    print(json.dumps(result,sort_keys=True),flush=True)

if __name__=='__main__':
    for q in (1,2,4):run(q)
    print('NEW EXACT ALGEBRAIC DOMAIN CONTROLS PASSED',flush=True)
