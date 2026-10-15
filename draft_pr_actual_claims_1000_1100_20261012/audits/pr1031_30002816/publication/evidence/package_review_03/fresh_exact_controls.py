from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import json,hashlib,datetime
R=Path(__file__).resolve().parent;P=R.parent.parent/'publication';pairs=list(combinations(range(6),2))
def req(c,m):
 if not c:raise RuntimeError(m)
def ga(a,b):return a[0]+b[0],a[1]+b[1]
def gm(a,b):return a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def gc(a):return a[0],-a[1]
def add(o,k,v):
 v=ga(o.get(k,(F(0),F(0))),v)
 if v!=(0,0):o[k]=v
 else:o.pop(k,None)
def wedge(a,b):
 o={}
 for k,x in a.items():
  for l,y in b.items():
   if k&l:continue
   inv=sum(1 for i in range(12) if k>>i&1 for j in range(12) if l>>j&1 and i>j)
   s=(-1)**inv;add(o,k|l,gm(x,(s*y[0],s*y[1])))
 return o
w=[{1<<(2*j):(F(1),F(0)),1<<(2*j+1):(F(0),F(-1))} for j in range(6)]
bar=lambda a:{k:gc(v) for k,v in a.items()}
cols=[];labels=[]
raw={}
for a,(i,j) in enumerate(pairs):
 for b,(k,l) in enumerate(pairs):raw[a,b]={mask:(x/4,y/4) for mask,(x,y) in wedge(wedge(w[i],w[j]),wedge(bar(w[k]),bar(w[l]))).items()}
for kind,a,b in [('diag',i,i) for i in range(15)]+[(kind,a,b) for a,b in combinations(range(15),2) for kind in ('real','imag')]:
 o={}
 for m,v in raw[a,b].items():add(o,m,gm(v,(0,1)) if kind=='imag' else v)
 if kind!='diag':
  for m,v in raw[b,a].items():add(o,m,gm(v,(0,-1)) if kind=='imag' else v)
 req(all(y==0 for x,y in o.values()),'reality');cols.append({m:x for m,(x,y) in o.items()});labels.append([kind,a,b])
cert=json.loads((P/'checks/EMBEDDING_CERTIFICATE.json').read_text())
for n,c in enumerate(cert['columns']):
 a={sum(1<<i for i in k):F(v) for k,v in c['entries']}
 req(c['label']==labels[n] and a==cols[n],'certificate column '+str(n))
gram=0
for i,a in enumerate(cols):
 for j in range(i,225):
  req(sum(x*cols[j].get(m,0) for m,x in a.items())==(1 if i<15 else 2) if i==j else sum(x*cols[j].get(m,0) for m,x in a.items())==0,'gram')
  gram+=1
phi_masks={sum(1<<t for t in (2*i,2*i+1,2*j,2*j+1)) for i,j in pairs}
q_masks={sum(1<<t for t in (2*i,2*i+1,2*j,2*j+1)) for i,j in pairs if j<3 or i>=3}
evalform=lambda c,m:sum(v for k,v in c.items() if k in m)
for n,c in enumerate(cols):
 kind,a,b=labels[n];i,j=pairs[a]
 req(evalform(c,phi_masks)==(1 if kind=='diag' else 0),'phi')
 req(evalform(c,q_masks)==(1 if kind=='diag' and (j<3 or i>=3) else 0),'q')
def image(z):
 o={}
 for n,(kind,a,b) in enumerate(labels):
  h=gm(z[a],gc(z[b]));scale=h[1] if kind=='imag' else h[0]
  for m,v in cols[n].items():add(o,m,(scale*v,F(0)))
 return {m:x for m,(x,y) in o.items() if x}
def biv(a,b):return [ga(gm(a[i],b[j]),gm((-a[j][0],-a[j][1]),b[i])) for i,j in pairs]
def rv(a):return {1<<(2*j+v):(x,F(0)) for j,(r,i) in enumerate(a) for v,x in [(0,r),(1,i)] if x}
def ja(a):return [(-i,r) for r,i in a]
frames=[]
for k in range(12):
 a=[(F(((j+1)*(k+2))%7-3,1+(k%3)),F(((j+2)*(k+1))%5-2,1+(k%2))) for j in range(6)]
 b=[(F(((j+3)*(k+4))%11-5,1+((k+1)%3)),F(((j+4)*(k+3))%7-3,1+((k+1)%2))) for j in range(6)]
 z=biv(a,b);actual=image(z)
 expected=wedge(wedge(wedge(rv(a),rv(ja(a))),rv(b)),rv(ja(b)))
 req(actual=={m:x for m,(x,y) in expected.items()},'frame '+str(k))
 frames.append({'id':k,'nonzero_coordinates':len(actual),'all495_match':True})
# Phase invariance, zero wedge and reversed pure orientation.
z=[(F(0),F(0))]*15;z[0]=(F(1),F(0));a=image(z)
req(image([(F(-y),F(x)) for x,y in z])==a,'phase');req(evalform(a,phi_masks)==1 and evalform(a,q_masks)==1,'pure plane')
rev={m:-v for m,v in a.items()};req(evalform(rev,phi_masks)==-1 and evalform(rev,q_masks)==-1,'Q global sign')
req(image([(F(0),F(0))]*15)=={},'zero wedge')
# Rational normalized rank-two mixed tensor, ambient equations but nonseparable.
z=[(F(0),F(0))]*15;z[pairs.index((0,3))]=(F(3,5),F(0));z[pairs.index((1,4))]=(F(4,5),F(0));a=image(z)
req(evalform(a,phi_masks)==1 and evalform(a,q_masks)==0,'entangled equations')
minor=F(3,5)*F(4,5);pt=-2*minor;req(minor==F(12,25) and pt==F(-24,25),'PT')
# Real explicit sphere-norm completion -> affine SOS elementary identity.
for t in [F(-1),F(-3,5),F(0),F(3,5),F(1)]:req(F(1)-t==F(1,2)*(1-t)**2+F(1,2)*(1-t*t),'completion identity')
# Rational strict gap Lipschitz bound, c' nonzero and positive delta are deductive.
d={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'implementation':'Independent sparse rational Gaussian bit-mask wedge; no candidate checker imported','all225_certificate_columns_equal':True,'gram_upper_entries':gram,'ambient_inverse':'orthogonal columns with norms 1 (15) and 2 (210), so diag(norms)^-1 A^T extends to ambient','Phi_Q_all225':True,'rational_complex_frames':frames,'phase_invariance':True,'zero_wedge':True,'reverse_pure_Phi_Q':[-1,-1],'entangled_normalized_mixed_projector':{'Phi':1,'Q':0,'mixed_minor':str(minor),'partial_transpose_witness':str(pt),'implication':'Equations alone admit this projector; PSD mixed support is insufficient for Sep or C membership.'},'completion_algebra_cases':5,'certificate_sha256':hashlib.sha256((P/'checks/EMBEDDING_CERTIFICATE.json').read_bytes()).hexdigest()}
(R/'FRESH_EXACT_CONTROLS.json').write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d,indent=2))
