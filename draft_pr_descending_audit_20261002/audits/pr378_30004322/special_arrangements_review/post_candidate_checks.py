"""Post-exposure checks using the already sealed independent exact field/geometry."""
from independent_exact_checks import *
from itertools import combinations
from collections import Counter

print('POST_CANDIDATE_EXPOSURE: these checks do not alter the independent seal.')
H=list(map(norm,[(1,0,0),(0,1,0),(0,0,1)]+[(U,W**i,W**j) for i in range(3) for j in range(3)]))
Fermat=list(map(norm,[(U,-W**i,O) for i in range(3)]+[(O,U,-W**i) for i in range(3)]+[(-W**i,O,U) for i in range(3)]))
pts,r=singular(H);joins,masks=joined(pts)
y=[F(1,6) if ri==4 else F(1,4) for ri in r]
cost=12*F(1,4)+9*F(1,6)
assert cost==sum(y)==F(9,2)
for p,ri in zip(pts,r):
    coverage=sum(F(1,4) for l in H if dot(l,p)==0)+sum(F(1,6) for l in Fermat if dot(l,p)==0)
    assert coverage==1
    print('HESSE_PRIMAL',coords(p),'r',ri,'coverage',coverage)
dual_loads=[]
for l,m in zip(joins,masks):
    load=sum(y[i] for i in range(len(pts)) if m&(1<<i))
    assert load<=1
    dual_loads.append(load)
    print('HESSE_GLOBAL_DUAL',coords(l),'points',m.bit_count(),'load',load)
assert Counter(dual_loads)=={F(5,12):36,F(1):21}
print('HESSE_COST',cost,'GLOBAL_DUAL_LOAD_HISTOGRAM',dict(Counter(dual_loads)),'NONLINEAR_RATIO',F(1)/cost)
print('GLOBAL_DUAL_COMPLETENESS: all >=2-point lines enumerated; any other line has load <=1/4.')

# A complete quadrilateral modular base with a point P and non-pencil components.
P=norm((0,0,1))
base=set(map(norm,[(1,0,0),(0,1,0),(1,-1,0),(0,0,1),(1,0,-1),(0,1,-1)]))
old,rr=singular(list(base))
assert all(any(dot(l,p)==0 for l in base if dot(l,P)==0) for p in old)
pool=list(map(norm,[(2,3,5),(3,-2,7),(5,1,-4),(1,1,-2),(2,-1,0),(0,1,-2),(1,0,-3),(1,-1,1)]))
branches=Counter();cases=0
for adds in [()]+[(a,) for a in pool]+list(combinations(pool,2)):
    arr=base|set(adds);Z,rs=singular(list(arr));span,sm=joined(Z)
    pencil={l for l in arr if dot(l,P)==0};m=len(pencil)
    new={l for l in arr-base if dot(l,P)!=0};t=len(new)
    outside=[p for p in Z if all(dot(l,p)!=0 for l in pencil)]
    ka=max(sum(dot(l,p)==0 for p in Z) for l in arr)
    if not outside:cover=set(pencil);branch='pencil'
    elif ka>=m+t:cover=pencil|new;branch='full_added'
    else:
        assert t==2 and len(outside)<=2 and ka>=m+1
        aux=cross(*outside) if len(outside)==2 else next(l for l in new if dot(l,outside[0])==0)
        cover=pencil|{aux};branch='join'
    assert len(cover)<=ka
    assert all(any(dot(l,p)==0 for l in cover) for p in Z)
    k=max(mask.bit_count() for mask in sm)
    support=cover|arr
    ks=max(sum(dot(l,p)==0 for p in Z) for l in support)
    assert ks==k
    for l,mask in zip(span,sm):
        assert mask.bit_count()<=ks
        if l not in cover:assert mask.bit_count()<=len(cover)
    print('TWO_EXTENSION_COORDINATE_CONTROL',cases,'added',[coords(a) for a in adds],'pencil_m',m,'outside',[coords(p) for p in outside],'kA',ka,'mpl_ALL',k,'cover_lines',[coords(l) for l in sorted(cover,key=coords)],'branch',branch)
    branches[branch]+=1;cases+=1
print('TWO_EXTENSION_TOTAL',cases,'BRANCHES',dict(branches))
print('DONE exact candidate-focused checks passed.')
