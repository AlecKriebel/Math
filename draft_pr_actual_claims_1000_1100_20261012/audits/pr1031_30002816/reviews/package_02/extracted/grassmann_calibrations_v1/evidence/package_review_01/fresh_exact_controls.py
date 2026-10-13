"""Fresh independent bit-mask exterior algebra, exact rational control program."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import json,datetime,hashlib
R=Path(__file__).resolve().parent;P=R.parent.parent/'publication'
# Exact Gaussian rational arithmetic, no imported candidate routines.
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def mul(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def conj(a):return (a[0],-a[1])
def scale(a,s):return (a[0]*s,a[1]*s)
def wedge(a,b):
 out={}
 for x,c in a.items():
  for y,d in b.items():
   if x&y:continue
   inv=sum((y&((1<<j)-1)).bit_count() for j in range(12) if x&(1<<j))
   m=x|y;v=add(out.get(m,(0,0)),scale(mul(c,d),(-1)**inv))
   if v!=(0,0):out[m]=v
   else:out.pop(m,None)
 return out
def sumext(a,b,s=1):
 out=dict(a)
 for m,v in b.items():
  v=add(out.get(m,(0,0)),scale(v,s))
  if v!=(0,0):out[m]=v
  else:out.pop(m,None)
 return out
def need(x,label):
 if not x:raise RuntimeError(label)
pairs=list(combinations(range(6),2));ws=[{1<<(2*j):(1,0),1<<(2*j+1):(0,-1)} for j in range(6)];bars=[{m:conj(v) for m,v in w.items()} for w in ws]
uw=[wedge(ws[i],ws[j]) for i,j in pairs];ub=[wedge(bars[i],bars[j]) for i,j in pairs]
raw={(a,b):wedge(uw[a],ub[b]) for a in range(15) for b in range(15)}
cert=json.loads((P/'checks/EMBEDDING_CERTIFICATE.json').read_text());cols=[];labels=[]
for c in cert['columns']:
 kind,a,b=c['label'];v=raw[a,b]
 if kind=='real':v=sumext(v,raw[b,a])
 if kind=='imag':v={m:mul((0,1),z) for m,z in sumext(v,raw[b,a],-1).items()}
 v={m:scale(z,F(1,4)) for m,z in v.items()};need(all(z[1]==0 for z in v.values()),'reality');v={m:z[0] for m,z in v.items()}
 target={sum(1<<i for i in inds):F(value) for inds,value in c['entries']}
 need(v==target,'225 coordinate columns');cols.append(v);labels.append(c['label'])
gram_count=0
for a,v in enumerate(cols):
 for b in range(a,len(cols)):
  g=sum(c*cols[b].get(m,0) for m,c in v.items());want=(1 if labels[a][0]=='diag' else 2) if a==b else 0
  need(g==want,'Gram/rank/isometry');gram_count+=1
phimasks=[sum(1<<j for j in (2*a,2*a+1,2*b,2*b+1)) for a,b in pairs];qmasks=[m for (a,b),m in zip(pairs,phimasks) if (a<3 and b<3) or a>=3]
def evalform(v,masks):return sum(v.get(m,0) for m in masks)
for lab,v in zip(labels,cols):
 kind,a,b=lab;i,j=pairs[a]
 need(evalform(v,phimasks)==(1 if kind=='diag' else 0),'PhiTrace')
 need(evalform(v,qmasks)==(1 if kind=='diag' and ((i<3 and j<3) or i>=3) else 0),'Qsupport')
def realvec(z):return {1<<(2*j+q):(z[j][q],0) for j in range(6) for q in range(2) if z[j][q]}
def Jvec(z):return realvec([(-v[1],v[0]) for v in z])
def projector_image(a,b):
 z=[add(mul(a[i],b[j]),scale(mul(a[j],b[i]),-1)) for i,j in pairs];out={}
 for lab,col in zip(labels,cols):
  kind,i,j=lab;h=mul(z[i],conj(z[j]));coeff=h[1] if kind=='imag' else h[0]
  for m,v in col.items():out[m]=out.get(m,0)+coeff*v
 return {m:v for m,v in out.items() if v}
rows=[]
for k in range(12):
 a=[(F((k+2*j)%7-3,k+1),F((2*k+j)%5-2,j+1)) for j in range(6)];b=[(F((3*k+j)%11-5,j+2),F((k+3*j)%7-3,k+2)) for j in range(6)]
 plane=wedge(wedge(wedge(realvec(a),Jvec(a)),realvec(b)),Jvec(b));plane={m:z[0] for m,z in plane.items()}
 need(projector_image(a,b)==plane,'all real plane coordinates');rows.append({'case':k,'nonzero_coordinates':len(plane),'identity':True})
# Pure Bell projector: hyperplanes alone accept it, product hull does not.
H=[[F(0) for _ in range(15)] for _ in range(15)];ids=[pairs.index((0,3)),pairs.index((1,4))]
for i in ids:
 for j in ids:H[i][j]=F(1,2)
out={}
for lab,col in zip(labels,cols):
 kind,i,j=lab;c=H[i][j] if kind!='imag' else 0
 for m,v in col.items():out[m]=out.get(m,0)+c*v
need(evalform(out,phimasks)==1 and evalform(out,qmasks)==0,'Bell hyperplanes')
# Partial transpose on mixed9 coordinates: v=|0,1>-|1,0> gives exactly -1.
rho={(0,0):F(1,2),(0,4):F(1,2),(4,0):F(1,2),(4,4):F(1,2)}
pt={(3*(i//3)+j%3,3*(j//3)+i%3):v for (i,j),v in rho.items()};v={1:1,3:-1};npt=sum(v.get(i,0)*c*v.get(j,0) for (i,j),c in pt.items());need(npt==-1,'entangled support counterexample')
# Negative orientation reverses Phi and Q on a pure complex plane.
first=cols[0];negative={m:-v for m,v in first.items()};need(evalform(negative,phimasks)==-1 and evalform(negative,qmasks)==-1,'Q not nonnegative on massball')
# Rational noncomplex oriented unit frame e1,(3f1+4e2)/5,e3,f3.
a={1:(1,0)};b={2:(F(3,5),0),4:(F(4,5),0)};c={16:(1,0)};d={32:(1,0)};p=wedge(wedge(wedge(a,b),c),d);p={m:z[0] for m,z in p.items()};need(sum(v*v for v in p.values())==1 and evalform(p,phimasks)==F(3,5),'strict Wirtinger boundary')
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','mechanism':'independently authored Gaussian rational bit-mask wedge multiplication; no candidate routine import','columns':225,'gram_entries':gram_count,'rank':225,'phi_trace':True,'q_trace':True,'general_rational_frames':rows,'bell_hyperplanes':[1,0],'bell_partial_transpose_test_vector_value':str(npt),'Q_negative_on_mass_ball':True,'rational_noncomplex_unit_plane_Phi':'3/5','limitations':'finite frame controls supplement a full written universal derivation; no Fawzi reproof or explicit failing calibration'}
(R/'receipts/FRESH_EXACT_CONTROLS.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
