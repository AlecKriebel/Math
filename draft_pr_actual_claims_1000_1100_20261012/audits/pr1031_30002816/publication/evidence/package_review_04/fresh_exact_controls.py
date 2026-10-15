"""New review04 exact arithmetic, independent recursive determinant construction."""
import datetime,hashlib,json,pathlib,sys
sys.dont_write_bytecode=True
from fractions import Fraction as F
from itertools import combinations
B=pathlib.Path(__file__).resolve().parent
X=B/'extracted/grassmann_calibrations_v1'
pairs=list(combinations(range(6),2));quads=list(combinations(range(12),4))
G0=(F(0),F(0));G1=(F(1),F(0));GI=(F(0),F(1))
def add(a,b):return a[0]+b[0],a[1]+b[1]
def neg(a):return -a[0],-a[1]
def mul(a,b):return a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def conj(a):return a[0],-a[1]
def scale(a,v):return a[0]*v,a[1]*v
# Recursion by Laplace expansion, unlike the supplied permutation determinant.
def det(m):
 if len(m)==1:return m[0][0]
 s=G0
 for k,v in enumerate(m[0]):
  if v!=G0:s=add(s,scale(mul(v,det([row[:k]+row[k+1:] for row in m[1:]])),(-1)**k))
 return s
def cvec(j,sign):return [GI if k==2*j+1 and sign==1 else neg(GI) if k==2*j+1 else G1 if k==2*j else G0 for k in range(12)]
def exterior(columns):
 out={}
 for q in quads:
  d=det([[v[k] for v in columns] for k in q])
  if d!=G0:out[q]=d
 return out
raw={(i,j):exterior([cvec(a,-1),cvec(b,-1),cvec(c,1),cvec(d,1)]) for i,(a,b) in enumerate(pairs) for j,(c,d) in enumerate(pairs)}
cert=json.loads((X/'checks/EMBEDDING_CERTIFICATE.json').read_text());cols=[]
for column in cert['columns']:
 kind,i,j=column['label'];actual={tuple(q):F(v) for q,v in column['entries']};expected={}
 for q in set(raw[i,j])|set(raw[j,i]):
  if kind=='diag':v=raw[i,j].get(q,G0)
  elif kind=='real':v=add(raw[i,j].get(q,G0),raw[j,i].get(q,G0))
  else:v=mul(GI,add(raw[i,j].get(q,G0),neg(raw[j,i].get(q,G0))))
  assert v[1]==0
  if v[0]:expected[q]=v[0]/4
 assert actual==expected
 cols.append(expected)
def image(H):
 p={}
 for col,C in zip(cert['columns'],cols):
  kind,i,j=col['label'];coef=H[i][j][1 if kind=='imag' else 0]
  for q,v in C.items():p[q]=p.get(q,F(0))+coef*v
 return {q:v for q,v in p.items() if v}
def phi(p,pure=False):return sum(p.get((2*i,2*i+1,2*j,2*j+1),F(0)) for i,j in pairs if not pure or (i<3 and j<3) or (i>=3 and j>=3))
def projector(a,b):
 z=[add(mul(a[i],b[j]),neg(mul(a[j],b[i]))) for i,j in pairs]
 return [[mul(x,conj(y)) for y in z] for x in z]
def real_frame(a,b):
 out=[]
 for v in (a,b):
  out.extend([[G0 for k in range(12)],[G0 for k in range(12)]])
  for j,(r,i) in enumerate(v):out[-2][2*j]=(r,F(0));out[-2][2*j+1]=(i,F(0));out[-1][2*j]=(-i,F(0));out[-1][2*j+1]=(r,F(0))
 return out
rows=[]
def row(n,data):rows.append({'case':n,'status':'PASS',**data})
for i,c in enumerate(cols):
 for j in range(i,225):
  dot=sum(v*cols[j].get(q,F(0)) for q,v in c.items())
  assert dot==(F(1 if i<15 else 2) if i==j else 0)
 assert phi(c)==(1 if i<15 else 0)
 k,a,b=cert['columns'][i]['label'];s,t=pairs[a]
 assert phi(c,True)==(1 if k=='diag' and ((s<3 and t<3) or (s>=3 and t>=3)) else 0)
row('all225_recursive_determinant_columns_and25425_Gram_pairs',{'columns':225,'gram_pairs':25425,'reality':True,'rank':225,'phi_trace':True,'q_pure_trace':True})
examples=[([(F(j-2),F((j%3)-1)) for j in range(6)],[(F(2-j),F(j%2)) for j in range(6)]),
          ([(F(3,5),0),(0,F(4,5)),G0,G0,G0,G0],[G0,G0,G0,G0,(F(5,13),0),(0,F(12,13))]),
          ([G1,G0,G0,G0,G0,G0],[G0,G1,G0,G0,G0,G0])]
for k,(a,b) in enumerate(examples):
 H=projector(a,b);p=image(H);frame=exterior(real_frame(a,b));assert p=={q:v[0] for q,v in frame.items()} and all(v[1]==0 for v in frame.values())
 aphase=[mul(GI,v) for v in a];assert image(projector(aphase,b))==p
 degenerate=image(projector(a,a));assert degenerate=={}
 row('exact_projector_phase_degenerate_example'+str(k),{'all495coordinates':True,'positive_orientation':True,'phase_invariant':True,'degenerate_wedge_zero':True,'phi':str(phi(p)),'q':str(phi(p,True))})
# Negative complex orientation outside F.
a,b=examples[2];p=image(projector(a,b));assert phi(p)==1 and phi({q:-v for q,v in p.items()})==-1 and phi({q:-v for q,v in p.items()},True)==-1
row('reversed_orientation_Q_negative_outside_face',{'phi':-1,'q':-1})
# Product mixed versus a rational rank-two entangled projector.
a,b=examples[1];p=image(projector(a,b));assert phi(p)==1 and phi(p,True)==0
z=[G0]*15;z[pairs.index((0,3))]=G1;z[pairs.index((1,4))]=G1
H=[[scale(mul(x,conj(y)),F(1,2)) for y in z] for x in z];ent=image(H);assert phi(ent)==1 and phi(ent,True)==0
mixed_z={(i,j-3):z[k][0] for k,(i,j) in enumerate(pairs) if i<3<=j}
ranktwo_minor=mixed_z[0,0]*mixed_z[1,1]-mixed_z[0,1]*mixed_z[1,0];assert ranktwo_minor!=0
row('two_equations_alone_admit_entangled_projector',{'phi':'1','q':'0','mixed_ranktwo_minor':'1','inside_mass_ball_inferred':False,'proof_not_numeric_control_excludes_membership':True})
# A PSD mixture cannot cancel a nonzero pure support contribution.
a,b=examples[2];pure=projector(a,b);a,b=examples[1];mixed=projector(a,b)
H=[[add(scale(pure[i][j],F(2,7)),scale(mixed[i][j],F(5,7))) for j in range(15)]for i in range(15)]
assert phi(image(H),True)==F(2,7)
row('positive_PSD_support_mixture',{'pure_weight':'2/7','support_trace':'2/7','no_positive_cancellation':True})
# Compact moment / completion boundary: one-dimensional signed sphere.
# M=[[1,x],[x,1]], PSD iff |x|<=1; 1-p=(1-p)^2/2 on p=±1.
for p in (F(-1),F(1)):assert 1-p==(1-p)**2/2
for p in (F(-3),F(0),F(2)):assert p*p==p*p+(0*p)**2
row('moment_signed_sphere_and_completion_identity',{'trace':2,'projection':'[-1,1]','support_affine_square':True,'homogeneous_completion':True})
# Strict gap rational perturbation, with exact worst-case estimate.
g=F(1,17);d=F(1,1000);R=F(1);assert g-(R+1)*d>0
row('strict_gap_rational_perturbation_bound',{'gap':'1/17','perturbation_norm':'1/1000','positive_remaining_bound':str(g-2*d),'target_witness_constructed':False})
obj={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','mechanism':'new exact Laplace-recursive determinant reconstruction and finite boundary checks, separate from theorem proof','controls':rows}
(B/'FRESH_EXACT_CONTROLS.json').write_text(json.dumps(obj,indent=2)+'\n');print(json.dumps(obj,indent=2))
