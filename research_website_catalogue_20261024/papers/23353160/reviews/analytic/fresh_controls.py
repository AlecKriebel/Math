"""Exact controls written before reading the supplied verifier implementations.

Gaussian rational exterior arithmetic constructs A. Determinants independently
construct real four-frame coordinates. A modular rank certificate proves the
full rational-linear rank (not merely rank on sampled pure projectors).
"""
from fractions import Fraction as F
from itertools import combinations, permutations
from pathlib import Path
import json,random,datetime,hashlib,time
START=time.time();checks=[]
def chk(name,ok,evidence=None):
    assert ok,(name,evidence)
    checks.append({'name':name,'passed':True,'evidence':evidence})
def g(a=0,b=0):return (F(a),F(b))
O=g();E=g(1);J=g(0,1)
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def neg(a):return (-a[0],-a[1])
def conj(a):return (a[0],-a[1])
def mul(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def scale(a,c):return (a[0]*c,a[1]*c)
def wedge(a,b):
    out={}
    for ia,ca in a.items():
        for ib,cb in b.items():
            if set(ia)&set(ib):continue
            s=(-1)**sum(x>y for x in ia for y in ib);k=tuple(sorted(ia+ib))
            out[k]=add(out.get(k,O),scale(mul(ca,cb),s))
    return {k:v for k,v in out.items() if v!=O}
def wedges(xs):
    out={():E}
    for x in xs:out=wedge(out,x)
    return out
def linadd(out,x,c):
    for k,v in x.items():out[k]=add(out.get(k,O),mul(v,c))
def clean(x):return {k:v for k,v in x.items() if v!=O}
pairs=list(combinations(range(6),2));four=list(combinations(range(12),4))
w=[{(2*i,):E,(2*i+1,):neg(J)} for i in range(6)]
w2=[wedge(w[i],w[j]) for i,j in pairs]
raw={(i,j):wedge(w2[i],{k:conj(v) for k,v in w2[j].items()}) for i in range(15) for j in range(15)}
def amap(H):
    out={}
    for (i,j),v in H.items():linadd(out,raw[i,j],scale(v,F(1,4)))
    return clean(out)
def phi(a):return sum(a.get((2*i,2*i+1,2*j,2*j+1),O)[0] for i,j in pairs)
def q(a):return sum(a.get((2*i,2*i+1,2*j,2*j+1),O)[0] for i,j in pairs if (i<3)==(j<3))
bases=[]
for i in range(15):bases.append({(i,i):E})
for i,j in combinations(range(15),2):
    bases.append({(i,j):E,(j,i):E});bases.append({(i,j):J,(j,i):neg(J)})
images=[amap(H) for H in bases]
chk('all 225 Hermitian basis images are real',all(v[1]==0 for a in images for v in a.values()),225)
chk('Phi equals trace on full Hermitian basis',all(phi(a)==sum(v[0] for (i,j),v in H.items() if i==j) for a,H in zip(images,bases)),225)
pure={i for i,(a,b) in enumerate(pairs) if (a<3)==(b<3)}
chk('Q equals pure-block trace on full Hermitian basis',all(q(a)==sum(v[0] for (i,j),v in H.items() if i==j and i in pure) for a,H in zip(images,bases)),225)
# Sparse exact elimination modulo 101; all denominators here divide four.
rows={};pivots=[]
for a in images:
    row={four.index(k):int((v[0]*4))%101 for k,v in a.items() if v[0]}
    while row:
        k=min(row);v=row[k]
        if k not in rows:
            inv=pow(v,-1,101);rows[k]={j:x*inv%101 for j,x in row.items()};pivots.append(k);break
        for j,x in rows[k].items():
            row[j]=(row.get(j,0)-v*x)%101
            if not row[j]:del row[j]
chk('rational map has full rank via F101 certificate',len(rows)==225,{'rank':len(rows),'pivots':pivots})

perms=[(t,(-1)**sum(t[i]>t[j] for i in range(4) for j in range(i+1,4))) for t in permutations(range(4))]
def det4(M):return sum(s*M[0][t[0]]*M[1][t[1]]*M[2][t[2]]*M[3][t[3]] for t,s in perms)
def frame_wedge(a,b):
    ar=[v for c in a for v in c];br=[v for c in b for v in c]
    ja=[v for c in a for v in (-c[1],c[0])];jb=[v for c in b for v in (-c[1],c[0])]
    cols=[ar,ja,br,jb];out={}
    for inds in four:
        value=det4([[c[i] for c in cols] for i in inds])
        if value:out[inds]=g(value)
    return out
def plucker(a,b):return [add(mul(a[i],b[j]),neg(mul(a[j],b[i]))) for i,j in pairs]
def outer(z,factor=F(1)):return {(i,j):scale(mul(x,conj(y)),factor) for i,x in enumerate(z) for j,y in enumerate(z) if x!=O and y!=O}
rng=random.Random(23353160)
for trial in range(12):
    a=[g(F(rng.randrange(-3,4),rng.randrange(1,4)),F(rng.randrange(-3,4),rng.randrange(1,4))) for _ in range(6)]
    b=[g(F(rng.randrange(-3,4),rng.randrange(1,4)),F(rng.randrange(-3,4),rng.randrange(1,4))) for _ in range(6)]
    z=plucker(a,b);mapped=amap(outer(z));direct=frame_wedge(a,b)
    chk('projector identity full 495 coordinates frame '+str(trial),mapped==direct,{'coordinates':495,'rational_nonorthonormal':True})
    chk('phase invariance frame '+str(trial),amap(outer([mul(J,t) for t in z]))==mapped)
    chk('trace agrees squared bivector norm frame '+str(trial),phi(mapped)==sum(mul(x,conj(x))[0] for x in z))
# Coordinate orientation and scaling mutations must be rejected.
H0={(0,0):E};a0=amap(H0)
chk('positive complex coordinate orientation',a0=={(0,1,2,3):E})
chk('negative orientation lies outside positive face and Q need not be globally nonnegative',phi({k:neg(v) for k,v in a0.items()})==-1 and q({k:neg(v) for k,v in a0.items()})==-1)
chk('doubling the map fails normalization',phi({k:scale(v,2) for k,v in a0.items()})==2)

# All mixed Plucker equations equal signed two-by-two matrix minors, using
# arbitrary complex entries and a separately evaluated minor formula.
for trial in range(8):
    M=[[g(rng.randrange(-3,4),rng.randrange(-3,4)) for j in range(3)] for i in range(3)]
    z={(i,j+3):M[i][j] for i in range(3) for j in range(3)};zz=wedge(z,z)
    for i,k in combinations(range(3),2):
        for j,l in combinations(range(3),2):
            minor=add(mul(M[i][j],M[k][l]),neg(mul(M[i][l],M[k][j])))
            chk('mixed Plucker/minor '+str((trial,i,k,j,l)),zz.get((i,k,j+3,l+3),O)==scale(minor,-2))
# Pure entangled projector satisfies both exposing equations but cannot belong
# to K: rank-one positive sums would force every generator into its non-simple ray.
z=[E if ij in [(0,3),(1,4)] else O for ij in pairs];ent=amap(outer(z,F(1,2)))
zz=wedge({ij:z[i] for i,ij in enumerate(pairs) if z[i]!=O},{ij:z[i] for i,ij in enumerate(pairs) if z[i]!=O})
chk('two equations alone admit normalized entangled projector',phi(ent)==1 and q(ent)==0 and zz!={}, {'Phi':str(phi(ent)),'Q':str(q(ent)),'nonzero_Plucker':{str(k):[str(t) for t in v] for k,v in zz.items()}})
# Compact-moment and affine-square positive controls on the unit circle.
for t in [F(-5,3),F(-1),F(0),F(2,3),F(3)]:
    x=(1-t*t)/(1+t*t);y=2*t/(1+t*t)
    chk('norm completion affine SOS on rational circle '+str(t),x*x+y*y==1 and 1-x==F(1,2)*(1-x)**2+F(1,2)*y*y)
    chk('rank-one moment trace-two normalization '+str(t),1+x*x+y*y==2)
result={'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'checks':checks,'named_checks':len(checks),'all_passed':True,'arithmetic':'Gaussian rationals, exact determinant expansion, modular rank over F101','limitations':'Finite controls corroborate the analytic bridge and boundary cases; they do not prove Fawzi or construct the existential failing calibration.','runtime_seconds':time.time()-START}
Path(__file__).with_suffix('.results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':True,'checks':len(checks),'rank':len(rows),'seconds':time.time()-START},indent=2))
