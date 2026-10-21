from verify import flags, check
from fractions import Fraction as Q
import json
from pathlib import Path
P=Path(__file__).parent
# Convex square, triangulated using an interior vertex (1/3, 1/4).
coords=[(Q(0),Q(0)),(Q(1),Q(0)),(Q(1),Q(1)),(Q(0),Q(1)),(Q(1,3),Q(1,4))]
facets=[(0,1,4),(1,2,4),(2,3,4),(3,0,4)]
fs=sum([flags(t) for t in facets],[])
for slope in [Q(i,11) for i in range(-20,21)]:
    w=[x+slope*y for x,y in coords]
    def height(f):
        return sum(sum(w[v] for v in range(5) if face>>v&1)/face.bit_count() for face in f)/3
    order=sorted(fs,key=lambda f:(height(f),f))
    result=check(order,fs)
    if not result['valid']:
        data={'coordinates':[[str(x),str(y)] for x,y in coords],'facets':facets,'slope':str(slope),'ties':len(set(map(height,fs)))!=len(fs),'result':result,'order':order}
        (P/'failed_convex_sweep.json').write_text(json.dumps(data,indent=2));print(json.dumps(data,indent=2));break
else: print('No failed order in this family')
