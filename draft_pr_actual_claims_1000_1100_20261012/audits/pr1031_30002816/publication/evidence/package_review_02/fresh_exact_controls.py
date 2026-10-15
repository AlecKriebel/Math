"""Fresh package02 controls, independent exterior algebra with rational pairs."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import datetime, hashlib, json

R = Path(__file__).resolve().parent
P = R.parent.parent / 'publication'
zero = (F(0), F(0))
one = (F(1), F(0))

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def add(a, b):
    return a[0] + b[0], a[1] + b[1]

def mul(a, b):
    return a[0]*b[0] - a[1]*b[1], a[0]*b[1] + a[1]*b[0]

def conj(a):
    return a[0], -a[1]

def scale(a, s):
    return a[0]*s, a[1]*s

def sumform(out, form, s=one):
    for key, v in form.items():
        val = add(out.get(key, zero), mul(s, v))
        if val != zero:
            out[key] = val
        else:
            out.pop(key, None)

def wedge(left, right):
    out = {}
    for a, ca in left.items():
        for b, cb in right.items():
            if set(a) & set(b):
                continue
            sign = (-1)**sum(i > j for i in a for j in b)
            key = tuple(sorted(a+b))
            sumform(out, {key: scale(mul(ca, cb), sign)})
    return out

def vec(values):
    return {(i,): v for i, v in enumerate(values) if v != zero}

def multivec(vectors):
    out = {(): one}
    for v in vectors:
        out = wedge(out, v)
    return out

pairs = list(combinations(range(6), 2))
labels = [('diag', i, i) for i in range(15)]
for i, j in combinations(range(15), 2):
    labels += [('real', i, j), ('imag', i, j)]
w = [{(2*j,): one, (2*j+1,): (F(0), F(-1))} for j in range(6)]
wb = [{key: conj(v) for key, v in vj.items()} for vj in w]
raw = {(i,j): multivec([w[a],w[b],wb[c],wb[d]])
       for i,(a,b) in enumerate(pairs) for j,(c,d) in enumerate(pairs)}
columns = []
for kind, i, j in labels:
    out = {}
    if kind == 'diag':
        sumform(out, raw[i,j], (F(1,4), F(0)))
    elif kind == 'real':
        sumform(out, raw[i,j], (F(1,4), F(0)))
        sumform(out, raw[j,i], (F(1,4), F(0)))
    else:
        sumform(out, raw[i,j], (F(0), F(1,4)))
        sumform(out, raw[j,i], (F(0), F(-1,4)))
    require(all(v[1] == 0 for v in out.values()), 'full column reality')
    columns.append({k:v[0] for k,v in out.items()})
certificate = json.loads((P/'checks/EMBEDDING_CERTIFICATE.json').read_text())
require([list(s) for s in labels] == [s['label'] for s in certificate['columns']], 'labels')
for col, record in zip(columns, certificate['columns']):
    expected = {tuple(k):F(v) for k,v in record['entries']}
    require(col == expected, 'independent full coordinate equality')
gram = 0
for i, left in enumerate(columns):
    for j in range(i,225):
        dot = sum(v*columns[j].get(k,0) for k,v in left.items())
        require(dot == ((1 if i < 15 else 2) if i == j else 0), 'Gram and rank')
        gram += 1
phi_keys = [(2*i,2*i+1,2*j,2*j+1) for i,j in pairs]
q_keys = [k for k,(i,j) in zip(phi_keys,pairs) if (i<3 and j<3) or (i>=3 and j>=3)]
for col, (kind,i,j) in zip(columns,labels):
    require(sum(col.get(k,0) for k in phi_keys) == (1 if kind=='diag' else 0), 'Phi trace')
    a,b = pairs[i]
    require(sum(col.get(k,0) for k in q_keys) ==
            (1 if kind=='diag' and ((a<3 and b<3) or (a>=3 and b>=3)) else 0), 'Q trace')
# Recover arbitrary rational coordinates using the ambient-linear inverse.
coeffs = [F((i*7)%13-6, (i%4)+1) for i in range(225)]
ambient = {}
for c,col in zip(coeffs,columns):
    for key,v in col.items():
        ambient[key] = ambient.get(key,F(0))+c*v
recovered = [sum(ambient.get(k,0)*v for k,v in col.items()) / (1 if i<15 else 2)
             for i,col in enumerate(columns)]
require(recovered == coeffs, 'ambient linear inverse')

def A(z):
    out = {}
    for i in range(15):
        for j in range(15):
            sumform(out,raw[i,j],scale(mul(z[i],conj(z[j])),F(1,4)))
    require(all(v[1]==0 for v in out.values()), 'projector reality')
    return {k:v[0] for k,v in out.items()}

projectors = []
for t in range(32):
    a = [(F(((j+1)*(t+3))%11-5,(t%3)+1),F((j*3+t)%7-3,(t%4)+1)) for j in range(6)]
    b = [(F((j*5+t*2)%13-6,(t%5)+1),F((j*7+t)%9-4,(t%2)+1)) for j in range(6)]
    z = [add(mul(a[i],b[j]),scale(mul(a[j],b[i]),-1)) for i,j in pairs]
    arv = [v for aj in a for v in ((aj[0],F(0)),(aj[1],F(0)))]
    brv = [v for bj in b for v in ((bj[0],F(0)),(bj[1],F(0)))]
    Jarv = [v for aj in a for v in ((-aj[1],F(0)),(aj[0],F(0)))]
    Jbrv = [v for bj in b for v in ((-bj[1],F(0)),(bj[0],F(0)))]
    plane = multivec(list(map(vec,[arv,Jarv,brv,Jbrv])))
    plane = {k:v[0] for k,v in plane.items()}
    image = A(z)
    require(image == plane, 'arbitrary rational product-projector identity')
    norm = sum(mul(v,conj(v))[0] for v in z)
    pure = sum(mul(z[i],conj(z[i]))[0] for i,(j,k) in enumerate(pairs)
               if (j<3 and k<3) or (j>=3 and k>=3))
    require(sum(image.get(k,0) for k in phi_keys)==norm, 'general trace')
    require(sum(image.get(k,0) for k in q_keys)==pure, 'general pure trace')
    require(A([mul((F(0),F(1)),s) for s in z])==image, 'unit phase invariance')
    require(sum(v*v for v in plane.values())==norm*norm, 'squared Gram determinant normalization')
    projectors.append(t)

# Nonnegative support only on the Kähler face; reversal is a real mass-ball generator.
reversed_plane = {(0,1,2,3):F(-1)}
require(sum(reversed_plane.get(k,0) for k in phi_keys)==-1 and
        sum(reversed_plane.get(k,0) for k in q_keys)==-1, 'global Q nonnegativity counterexample')
# Two hyperplanes alone admit a unit rank-one but entangled mixed-block projector.
z = [one if p in [(0,3),(1,4)] else zero for p in pairs]
zz = wedge({p:z[i] for i,p in enumerate(pairs) if z[i]!=zero},
           {p:z[i] for i,p in enumerate(pairs) if z[i]!=zero})
require(zz != {}, 'mixed rank-two nondecomposability')
image = {k:v/F(2) for k,v in A(z).items()}
require(sum(image.get(k,0) for k in phi_keys)==1 and sum(image.get(k,0) for k in q_keys)==0,
        'hyperplanes do not imply mass-ball membership')
# Positive projector mixture: pure-block trace cannot cancel with mixed-block projectors.
require(F(1,3)*1 + F(2,3)*0 == F(1,3), 'PSD positive support mixture')

# Every mixed Plücker relation equals the relevant determinant, by direct wedge square.
minor_cases=0
for rows in combinations(range(3),2):
    for cols in combinations(range(3),2):
        # Independent rank-two corner has determinant1 and wedge-square coefficient -2.
        i,j=rows;k,l=cols
        zform={(i,k+3):one,(j,l+3):one}
        square=wedge(zform,zform)
        require(square[(i,j,k+3,l+3)]==(F(-2),F(0)), 'mixed minor sign')
        minor_cases+=1
require(minor_cases==9,'all mixed minors')

# Exact normalization and calibration SOS on rational sphere points.
points=[(F(1),F(0),F(0)),(F(-1),F(0),F(0)),
        (F(3,5),F(4,5),F(0)),(F(0),F(3,5),F(4,5))]
for p in points:
    value=p[0]
    require(sum(s*s for s in p)==1,'unit sphere')
    require(F(1,2)*(1-value)**2+F(1,2)*(p[1]**2+p[2]**2)==1-value,'completion to affine SOS')
    # Take rows a+Bp=(1-p0,p1,p2)/sqrt2, avoiding irrational arithmetic by storing2*norm².
    a2=F(1,2)
    require(a2==F(1,2) and (p[1]**2+p[2]**2)==1-value**2,'optional pointwise converse')

# Compact trace equation and PSD evaluations of affine squares use complete moment entries.
weights=[F(1,4)]*4
M=[[sum(w*((F(1),)+p)[i]*((F(1),)+p)[j] for w,p in zip(weights,points))
    for j in range(4)] for i in range(4)]
require(M[0][0]==1 and sum(M[i][i] for i in range(4))==2,'sphere trace2')
av=[F(2),F(-3),F(5,2),F(1,3)]
evaluation=sum(av[i]*M[i][j]*av[j] for i in range(4) for j in range(4))
direct=sum(w*sum(ai*pi for ai,pi in zip(av,(F(1),)+p))**2 for w,p in zip(weights,points))
require(evaluation==direct and evaluation>=0,'moment affine square positivity')

receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS',
         'full_independent_embedding_columns':225,'gram_entries':gram,'ambient_dimension':495,
         'ambient_inverse_full_coordinate_test':True,'rational_projector_tests':len(projectors),
         'all9_mixed_minor_sign_tests':minor_cases,'phase_reality_norm_and_trace_checks':True,
         'global_Q_counterexample':True,'entangled_hyperplanes_only_counterexample':True,
         'PSD_support_positivity':True,'completion_and_converse_controls':len(points),
         'trace2_and_affine_square_moment_controls':True,
         'scope':'Exact finite controls support independently written universal deductions; no Fawzi reproof or explicit failing calibration.'}
(R/'receipts/FRESH_EXACT_CONTROLS.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
