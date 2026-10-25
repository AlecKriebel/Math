"""Independent exact exterior-algebra/hostile-boundary controls.

No submitted Python, certificate, archived review, or sibling opinion is imported.
SymPy rational/imaginary arithmetic; exterior products use bitmask parity, not
the submitted checker's determinant algorithm. Finite controls are not a proof
of Fawzi's theorem or an explicit failing calibration.
"""
from itertools import combinations, product
from pathlib import Path
from collections import Counter
import json, random, sys
import sympy as s

counts=Counter()
def require(test, family):
    if not test:
        raise RuntimeError(family)
    counts[family]+=1
def clean(d):
    return {k:s.expand(v) for k,v in d.items() if s.expand(v)!=0}
def add(a,b,c=1):
    d=dict(a)
    for k,v in b.items(): d[k]=d.get(k,0)+c*v
    return clean(d)
def scale(a,c): return clean({k:c*v for k,v in a.items()})
def conj(a): return {k:s.conjugate(v) for k,v in a.items()}
def wedge(a,b):
    d={}
    for k,v in a.items():
        for l,w in b.items():
            if k&l: continue
            inversions=sum((l&((1<<i)-1)).bit_count() for i in range(k.bit_length()) if k&(1<<i))
            key=k|l;d[key]=d.get(key,0)+(-1)**inversions*v*w
    return clean(d)
def chain(*vectors):
    out={0:s.S.One}
    for v in vectors:out=wedge(out,v)
    return out
def basis(i):return {1<<i:s.S.One}
def vec(values):return {1<<i:s.sympify(v) for i,v in enumerate(values) if v!=0}
def norm2(a):return s.expand(sum(v*s.conjugate(v) for v in a.values()))
def inner(a,b):return s.expand(sum(v*s.conjugate(b.get(k,0)) for k,v in a.items()))
def realvec(a):return {1<<(2*j+r):v for j,c in enumerate(a) for r,v in enumerate((s.re(c),s.im(c))) if v!=0}
def jmap(a):
    out={}
    for k,v in a.items():
        i=k.bit_length()-1
        out[1<<(i+1 if i%2==0 else i-1)]=v*(1 if i%2==0 else -1)
    return out

pairs=list(combinations(range(6),2))
pairindex={p:i for i,p in enumerate(pairs)}
w=[{1<<(2*i):s.S.One,1<<(2*i+1):-s.I} for i in range(6)]
wb=[wedge(w[i],w[j]) for i,j in pairs]
raw={(i,j):scale(wedge(wb[i],conj(wb[j])),s.Rational(1,4)) for i in range(15) for j in range(15)}
def image(h):
    out={}
    for (i,j),v in h.items():
        if v:out=add(out,raw[i,j],v)
    return out
def projector(z):return {(i,j):s.expand(a*s.conjugate(b)) for i,a in enumerate(z) for j,b in enumerate(z) if a!=0 and b!=0}
def phi(p,pure=False):
    return s.expand(sum(p.get((3<<(2*i))|(3<<(2*j)),0) for i,j in pairs if not pure or (i<3)==(j<3)))

# Complete Hermitian basis: diagonal, real symmetric, imaginary skew-symmetric.
hb=[{(i,i):s.S.One} for i in range(15)]
for i,j in combinations(range(15),2):hb.extend([{(i,j):s.S.One,(j,i):s.S.One},{(i,j):s.I,(j,i):-s.I}])
columns=[image(h) for h in hb]
for i,col in enumerate(columns):
    require(all(s.im(v)==0 for v in col.values()),'all_225_columns_real')
    require(phi(col)==sum(hb[i].get((j,j),0) for j in range(15)),'all_225_trace_functionals')
    require(phi(col,True)==sum(hb[i].get((j,j),0) for j,(a,b) in enumerate(pairs) if (a<3)==(b<3)),'all_225_support_functionals')
    for j in range(i+1):
        require(inner(col,columns[j])==((1 if i<15 else 2) if i==j else 0),'complete_gram_injectivity')

rng=random.Random(23353160)
for case in range(30):
    a=[s.Integer(rng.randrange(-2,3))+s.I*rng.randrange(-2,3) for _ in range(6)]
    b=[s.Integer(rng.randrange(-2,3))+s.I*rng.randrange(-2,3) for _ in range(6)]
    z=[s.expand(a[i]*b[j]-a[j]*b[i]) for i,j in pairs]
    out=image(projector(z));ar=realvec(a);br=realvec(b)
    require(out==chain(ar,jmap(ar),br,jmap(br)),'complex_projector_real_plane_identity')
    require(phi(out)==sum(s.expand(t*s.conjugate(t)) for t in z),'nonorthogonal_trace_norm')
    require(image(projector([s.I*t for t in z]))==out,'phase_invariance')

# Symbolic Kähler-angle boundary: explicit orthonormal rational four-frames.
e=[basis(i) for i in range(12)]
for c,d in [(s.Rational(3,5),s.Rational(4,5)),(s.S.One,s.S.Zero),(s.S.Zero,s.S.One),(-s.S.One,s.S.Zero)]:
    for f,g in [(s.Rational(5,13),s.Rational(12,13)),(s.S.One,s.S.Zero),(s.S.Zero,s.S.One)]:
        p=chain(e[0],add(scale(e[1],c),scale(e[4],d)),e[6],add(scale(e[7],f),scale(e[10],g)))
        require(norm2(p)==1,'tilted_frames_unit')
        require(phi(p)==c*f and abs(c*f)<=1,'tilted_wirtinger_values')

# Equation-only entangled state: trace 1 and Q=0 are NOT mass-ball membership.
z=[s.S.Zero]*15
z[pairindex[0,3]]=1/s.sqrt(2);z[pairindex[1,4]]=1/s.sqrt(2)
h=projector(z);out=image(h)
require(phi(out)==1 and phi(out,True)==0 and norm2(out)==1,'entangled_equation_only_example')
zz={((1<<a)|(1<<b)):z[i] for i,(a,b) in enumerate(pairs) if z[i]!=0}
require(wedge(zz,zz)=={(1<<0)|(1<<1)|(1<<3)|(1<<4):-s.S.One},'entangled_nonzero_plucker')
rho=s.zeros(9)
for i,j in [(0,0),(0,4),(4,0),(4,4)]:rho[i,j]=s.Rational(1,2)
pt=s.zeros(9)
for i,j,k,l in product(range(3),repeat=4):pt[3*i+l,3*k+j]=rho[3*i+j,3*k+l]
v=s.zeros(9,1);v[1]=1/s.sqrt(2);v[3]=-1/s.sqrt(2)
require((v.T*pt*v)[0]==-s.Rational(1,2),'entangled_partial_transpose_witness')

# Positivity is necessary for the support inference; orientation matters too.
bad={(pairindex[0,1],pairindex[0,1]):s.S.One,(pairindex[1,2],pairindex[1,2]):-s.S.One,(pairindex[0,3],pairindex[0,3]):s.S.One}
require(phi(image(bad))==1 and phi(image(bad),True)==0 and bad[pairindex[1,2],pairindex[1,2]]<0,'indefinite_zero_trace_countercontrol')
pure=chain(e[0],e[1],e[2],e[3])
require(phi(scale(pure,-1))==-1 and phi(scale(pure,-1),True)==-1,'negative_orientation_and_global_Q_countercontrol')
require(phi(scale(pure,2))==2,'wrong_normalization_countercontrol')
require(chain(w[0],w[1],w[0],w[1])=={} and raw[0,0]!={},'missing_conjugation_countercontrol')
cx=[s.S.Zero]*15;cx[pairindex[0,3]]=1/s.sqrt(2);cx[pairindex[1,3]]=s.I/s.sqrt(2)
ch=projector(cx)
require(ch[pairindex[0,3],pairindex[1,3]]==-s.I/2 and any(v!=0 for k,v in image(ch).items()),'complex_not_real_state_countercontrol')
realpart={k:s.re(v) for k,v in ch.items()}
require(image(ch)!=image(realpart),'discarding_imaginary_coordinates_countercontrol')

# All binary mixed coefficient matrices plus complex examples. Check every
# coefficient of z wedge z against the 2x2 minors, not merely a rank sample.
minor_pairs=list(combinations(range(3),2))
examples=list(product((0,1),repeat=9))
examples += [tuple(s.Integer(rng.randrange(-2,3))+s.I*rng.randrange(-2,3) for _ in range(9)) for _ in range(64)]
for values in examples:
    z={(1<<i)|(1<<(3+j)):values[3*i+j] for i,j in product(range(3),repeat=2) if values[3*i+j]!=0}
    sq=wedge(z,z);expected={}
    for (i,k),(j,l) in product(minor_pairs,repeat=2):
        minor=s.expand(values[3*i+j]*values[3*k+l]-values[3*i+l]*values[3*k+j])
        if minor:expected[(1<<i)|(1<<k)|(1<<(3+j))|(1<<(3+l))]=-2*minor
    require(sq==expected,'mixed_plucker_all_coefficients')
    require((sq=={})==all(values[3*i+j]*values[3*k+l]==values[3*i+l]*values[3*k+j] for (i,k),(j,l) in product(minor_pairs,repeat=2)),'mixed_rank_one_iff')

# Affine squares are essential: a circle supplies an exact positive control.
t=s.symbols('t',real=True)
p=s.Matrix([(1-t*t)/(1+t*t),2*t/(1+t*t)])
a=s.Matrix([1/s.sqrt(2),0]);B=s.eye(2)/s.sqrt(2);B[0,0]=-1/s.sqrt(2)
require(s.simplify(((a+B*p).T*(a+B*p))[0]-(1-p[0]))==0,'affine_SOS_circle_positive')
P=s.eye(2)-a*a.T/(a.T*a)[0]
require(s.simplify(2*(p.T*B.T*P*B*p)[0]-(1-p[0]**2))==0,'completion_converse_positive')
require(s.simplify((1-p[0]**2)/2+(1-p[0])**2/2-(1-p[0]))==0,'completion_forward_positive')
require(s.expand((1-(-s.Symbol('x')))-(1-s.Symbol('x')))==2*s.Symbol('x'),'homogeneous_SOS_evenness_countercontrol')
M=s.zeros(3)
for pt,weight in [(s.Matrix([1,1,0]),s.Rational(1,3)),(s.Matrix([1,0,1]),s.Rational(2,3))]:M+=weight*pt*pt.T
require(s.trace(M)==2 and M[0,0]==1 and M[1,1]+M[2,2]==1,'moment_trace_compactness_control')
require((s.Matrix([1,-1,0]).T*M*s.Matrix([1,-1,0]))[0]/2+(s.Matrix([0,0,1]).T*M*s.Matrix([0,0,1]))[0]/2==1-M[0,1],'moment_SOS_evaluation_control')

result={'status':'PASS','arithmetic':'SymPy exact rational and imaginary; independent bitmask exterior algebra','python_optimization':sys.flags.optimize,'sympy_version':s.__version__,'total_checks':sum(counts.values()),'families':dict(counts),'scope':'Finite bridge/boundary controls, not Fawzi reproof, explicit failing calibration, or novelty certification','no_published_source_or_certificate_import':True}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
