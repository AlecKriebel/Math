#!/usr/bin/env python3
"""Post-exposure coordinate verification and stronger global-LP certificates.

The independent field implementation was sealed before candidate exposure.
This extension is explicitly candidate-derived and is not independent discovery.
"""
from exact_fermat_check import Field, Q, combinations, Counter, json


def subfamily(q):
    n=5*q
    F=Field(n)
    z,o=F.zero,F.one
    roots=[o]
    for _ in range(1,n):
        roots.append(F.mul(roots[-1],F.zeta))
    full={}
    for i,r in enumerate(roots):
        for j,v in enumerate(((o,F.neg(r),z),(z,o,F.neg(r)),(F.neg(r),z,o))):
            full[F.norm(v)]=(j,i)
    comps={L:label for L,label in full.items() if label[1]%5 in (0,2,3)}
    actual={F.norm(F.cross(a,b)) for a,b in combinations(comps,2)}
    vertices={F.norm(v) for v in ((o,z,z),(z,o,z),(z,z,o))}
    def incident(L,p):
        return F.add(F.add(F.mul(L[0],p[0]),F.mul(L[1],p[1])),F.mul(L[2],p[2]))==z
    grid={}
    for a in roots:
        for b in roots:
            p=F.norm((a,b,o))
            inc={L for L in comps if incident(L,p)}
            if len(inc)>=2:
                if len(inc)==2:
                    kind='double'
                elif all(comps[L][1]%5==0 for L in inc):
                    kind='000'
                else:
                    kind='023'
                grid[p]=kind
    assert actual==set(grid)|vertices
    types=Counter(grid.values())
    assert types=={'000':q*q,'double':6*q*q,'023':6*q*q}
    points=sorted(actual)
    comp_inc={L:{i for i,p in enumerate(points) if incident(L,p)} for L in comps}
    pair_inc={}
    for i,j in combinations(range(len(points)),2):
        L=F.norm(F.cross(points[i],points[j]))
        pair_inc.setdefault(L,set()).update((i,j))
    assert max(map(len,pair_inc.values()))==4*q+1
    assert all(len(I)==(3*q+1 if comps[L][1]%5==0 else 4*q+1) for L,I in comp_inc.items())
    assert all(len(I)<=2 for L,I in pair_inc.items() if L not in full)
    assert all(len(I)==q+1 for L,I in pair_inc.items() if L in full and L not in comps)
    old_primal={L:(Q(1,3) if label[1]%5==0 else Q(1,2)) for L,label in comps.items()}
    old_dual={i:(Q(1,q) if grid.get(p)=='000' else (Q(1,2*q) if grid.get(p)=='double' else Q(0))) for i,p in enumerate(points)}
    assert sum(old_primal.values())==sum(old_dual.values())==4*q
    assert all(sum(old_primal[L] for L in comps if i in comp_inc[L])>=1 for i in range(len(points)))
    assert all(sum(old_dual[i] for i in I)==1 for I in comp_inc.values())
    old_load=max(sum(old_dual[i] for i in I) for I in pair_inc.values())
    if q==1:
        assert old_load==Q(3,2)
        high=next(i for i,p in enumerate(points) if grid.get(p)=='000')
        doubles=[i for i,p in enumerate(points) if grid.get(p)=='double']
        aux={F.norm(F.cross(points[high],points[i])) for i in doubles}
        assert len(aux)==6 and not(aux&set(full))
        assert all(len(pair_inc[L])==2 for L in aux)
        primal={L:(Q(1,9) if label[1]%5==0 else Q(4,9)) for L,label in comps.items()}
        primal.update({L:Q(1,9) for L in aux})
        dual={i:({'000':Q(2,3),'double':Q(1,3),'023':Q(1,6)}.get(grid.get(p),Q(0))) for i,p in enumerate(points)}
        optimum=Q(11,3)
    else:
        assert old_load<=1
        primal,dual,optimum=old_primal,old_dual,Q(4*q)
    assert sum(primal.values())==sum(dual.values())==optimum
    cov=[sum(w for L,w in primal.items() if i in pair_inc[L]) for i in range(len(points))]
    loads=[sum(dual[i] for i in I) for I in pair_inc.values()]
    assert min(cov)>=1 and max(loads)<=1 and max(dual.values())<=1
    print(json.dumps({
        'q':q,'n':n,'field_degree':F.d,'actual_components':len(comps),
        'actual_singular_points':len(points),'grid_types':dict(sorted(types.items())),
        'distinct_all_pair_lines':len(pair_inc),
        'all_line_support_histogram':dict(sorted(Counter(map(len,pair_inc.values())).items())),
        'K_all_lines':4*q+1,'epsilon_by_proved_cover_criterion':str(Q(1,4*q+1)),
        'component_optimum':str(Q(4*q)),
        'candidate_component_dual_max_all_line_load':str(old_load),
        'all_line_optimum':str(optimum),'global_primal_coverage_range':list(map(str,(min(cov),max(cov)))),
        'global_dual_max_line_load':str(max(loads)),
        'q1_repair_extra_lines':6 if q==1 else 0,
        'exact_coordinate_certificates':'PASS'
    },sort_keys=True),flush=True)
    F.mul.cache_clear()
    F.inv.cache_clear()


if __name__=='__main__':
    for q in (1,2,3):
        subfamily(q)
    print('ALL SUBFAMILY EXACT COORDINATE AND GLOBAL LP CHECKS PASSED',flush=True)
