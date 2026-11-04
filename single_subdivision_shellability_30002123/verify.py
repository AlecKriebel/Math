from itertools import permutations
from fractions import Fraction
import json,hashlib
from pathlib import Path
P=Path(__file__).parent

def flags(vertices):
    return [tuple(sum(1<<v for v in p[:i]) for i in range(1,len(p)+1)) for p in permutations(vertices)]
def check(order, expected=None):
    canonical=[frozenset(f) for f in order]
    if not order or len(set(canonical)) != len(order) or any(len(f) != len(order[0]) or len(set(f)) != len(f) for f in order):
        return {'valid':False,'reason':'empty, duplicate, malformed, or nonpure facet list'}
    if expected is not None and set(canonical) != set(map(frozenset,expected)):
        return {'valid':False,'reason':'facet set does not equal expected complex'}
    # A simplex intersects the previous union in a pure codimension-one
    # nonempty proper boundary subcomplex exactly when its old intersections
    # are all contained in old ridges and there is an old ridge, but not all.
    prior=[]
    for i,f in enumerate(order):
        f=set(f)
        if i:
            ints=[f & g for g in prior]
            ridges=[h for h in ints if len(h)==len(f)-1]
            if not ridges or any(not any(h<=r for r in ridges) for h in ints) or len(set(map(frozenset,ridges)))==len(f):
                return {'valid':False,'first_bad_index':i,'facet':sorted(f),'old_ridges':list(map(sorted,ridges)),'uncovered_intersections':[sorted(h) for h in ints if not any(h<=r for r in ridges)]}
        prior.append(f)
    return {'valid':True,'facets':len(order)}

out={}
for d in range(1,6):
    fs=flags(range(d+1))
    out[f'simplex_d{d}_lex']=check(fs,fs)
    if d<=4:
        weights=[Fraction(2**v) for v in range(d+1)]
        def height(f):
            return sum(sum(weights[v] for v in range(d+1) if face>>v&1)/face.bit_count() for face in f)
        order=sorted(fs,key=lambda f:(height(f),f))
        out[f'simplex_d{d}_centroid_sweep']=check(order,fs)
        if not out[f'simplex_d{d}_centroid_sweep']['valid']:
            (P/f'failed_sweep_d{d}.json').write_text(json.dumps(order))
# Two 4-simplices meeting in a ridge, with convex bipyramid realization.
# Both maximal simplices can be shelled. Search compatible permutation
# vertex order for second block, keeping a prescribed first block.
f1=flags(range(5))
for p in permutations([0,1,2,3,5]):
    order=f1+flags(p)
    if check(order,f1+flags([0,1,2,3,5]))['valid']:
        out['two_4simplices']={'second_vertex_order':p,**check(order,f1+flags([0,1,2,3,5]))}
        (P/'two_4simplices_certificate.json').write_text(json.dumps(order))
        break
(P/'computation_results.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
