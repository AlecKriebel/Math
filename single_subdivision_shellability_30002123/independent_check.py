"""Independent face-union checker; does not import research implementation."""
from pathlib import Path
from itertools import combinations, product, permutations
from fractions import Fraction as Q
from collections import Counter
import json, hashlib
R=Path(__file__).resolve().parent
def require(ok):
    if not ok: raise RuntimeError('Independent exact verification failed')

def powerset(s):
    s=tuple(s)
    return {frozenset(t) for k in range(len(s)+1) for t in combinations(s,k)}

def chains(top):
    # Enumerate maximal chains by extending one original vertex at each rank.
    out={frozenset()}
    for k in range(1,len(top)+1):
        nxt=set()
        faces=[sum(1<<v for v in t) for t in combinations(top,k)]
        for c in out:
            for f in faces:
                if all(x & f == x for x in c): nxt.add(c|{f})
        out=nxt
    return out

def audit(raw,tops):
    expected=set().union(*(chains(t) for t in tops))
    if not all(isinstance(f,list) and all(type(x) is int for x in f) for f in raw):return {'valid':False,'reason':'format'}
    fs=[frozenset(f) for f in raw]
    if any(len(f)!=len(tops[0]) or len(f)!=len(raw[i]) for i,f in enumerate(fs)):return {'valid':False,'reason':'facet cardinality'}
    if len(fs)!=len(set(fs)) or set(fs)!=expected:return {'valid':False,'reason':'facet set or multiplicity'}
    old=set(); ridge_counts=Counter()
    for i,f in enumerate(fs):
        faces=powerset(f); inter=faces & old
        if i:
            maximal={h for h in inter if not any(h<g for g in inter)}
            if not maximal or {len(h) for h in maximal}!={len(f)-1}:return {'valid':False,'reason':'nonpure intersection','first_bad_index':i,'maximal_intersections':[sorted(x) for x in maximal]}
            if len(maximal)==len(f):return {'valid':False,'reason':'whole boundary','first_bad_index':i}
            ridge_counts[len(maximal)]+=1
        old |= faces
    return {'valid':True,'facets':len(fs),'ridge_count_histogram':dict(sorted(ridge_counts.items())),'faces_including_empty':len(old)}

cert=json.loads((R/'two_4simplices_certificate.json').read_text())
tops=[(0,1,2,3,4),(0,1,2,3,5)]
result={'positive':audit(cert,tops)}
result['simplex_lex']={}
for d in range(1,6):
    order=[[sum(1<<v for v in perm[:k]) for k in range(1,d+2)] for perm in permutations(range(d+1))]
    result['simplex_lex'][str(d)]=audit(order,[tuple(range(d+1))])
require(all(x['valid'] for x in result['simplex_lex'].values()))
# Keep the complete facet set, but place a nonadjacent facet second.
wrong=cert.copy()
wrong[1],wrong[-1]=wrong[-1],wrong[1]
result['wrong_complete_order']=audit(wrong,tops)
require(not result['wrong_complete_order']['valid'])
mutations={'deleted_facet':cert[:-1],'duplicate_facet':cert+[cert[0]],'replaced_facet':cert[:-1]+[cert[0]],'unknown_face':[[99999]+cert[0][1:]]+cert[1:],'repeated_vertex':[[cert[0][1]]+cert[0][1:]]+cert[1:]}
result['tamper_tests']={k:audit(v,tops) for k,v in mutations.items()}
s=json.loads((R/'failed_convex_sweep.json').read_text())
coords=[tuple(map(Q,p)) for p in s['coordinates']]; slope=Q(s['slope'])
require(coords==[(Q(0),Q(0)),(Q(1),Q(0)),(Q(1),Q(1)),(Q(0),Q(1)),(Q(1,3),Q(1,4))])
require(s['facets']==[[0,1,4],[1,2,4],[2,3,4],[3,0,4]])
require(slope==Q(-14,11) and s['ties'] is False)
def h(flag):
    pts=[]
    for face in flag:
        vertices=[coords[v] for v in range(len(coords)) if (face>>v)&1]
        pts.append(sum(x+slope*y for x,y in vertices)/len(vertices))
    return sum(pts)/len(pts)
heights=list(map(h,s['order']))
result['square_fan']={'audit':audit(s['order'],s['facets']),'strictly_sorted':all(a<b for a,b in zip(heights,heights[1:])),'first_three_heights':list(map(str,heights[:3])),'interior_vertex':all(Q(0)<z<Q(1) for z in coords[4])}
real=json.loads((R/'realization.json').read_text())
v=[tuple(map(Q,p)) for p in real['vertices']]
require(real['facets']==[list(t) for t in tops])
require(v[:4]==[(Q(0),Q(0),Q(0),Q(0)),(Q(1),Q(0),Q(0),Q(0)),(Q(0),Q(1),Q(0),Q(0)),(Q(0),Q(0),Q(1),Q(0))])
p=tuple(sum(x[k] for x in v[:4])/4 for k in range(4))
require(all(v[4][k]+v[5][k]==2*p[k] for k in range(4)))
require(v[4][3]==1 and v[5][3]==-1)
# The determinants are +1 and -1 since the first three columns are e1,e2,e3.
result['realization']={'dimension':4,'oriented_determinants':[1,-1],'midpoint_ridge_barycentric_weights':['1/4']*4,'convex_union_verified':True}
result['input_hashes']={name:hashlib.sha256((R/name).read_bytes()).hexdigest() for name in ['two_4simplices_certificate.json','failed_convex_sweep.json','realization.json']}
require(result['positive']['valid'])
require(all(not v['valid'] for v in result['tamper_tests'].values()))
require(result['square_fan']['audit']['first_bad_index']==2)
require(result['square_fan']['strictly_sorted'])
print(json.dumps(result,indent=2))
(Path(__file__).parent/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
