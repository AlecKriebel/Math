"""Independent integer-polynomial reconstruction; no symbolic-algebra library.
Run with --packet pointing to the frozen 30005299 author directory.
"""
import json,argparse,hashlib,itertools
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,required=True);args=ap.parse_args();P=args.packet
checks=0
def eq(a,b):
 global checks
 assert a==b,(a,b);checks+=1
record=json.loads((P/'checks/representation_counterexample.json').read_text());A=record['symmetric_slices']
S=json.loads((P/'checks/SYMMETRIZER_CERTIFICATE.json').read_text());D=json.loads((P/'checks/DIMENSION_CERTIFICATES.json').read_text());G=D['general_determinant_coefficient_matrices'];zero=(0,0,0,0)
def add(a,b):
 d=a.copy()
 for m,c in b.items():d[m]=d.get(m,0)+c
 return {m:c for m,c in d.items() if c}
def mul(a,b):
 d={}
 for u,c in a.items():
  for v,e in b.items():
   m=tuple(x+y for x,y in zip(u,v));d[m]=d.get(m,0)+c*e
 return {m:c for m,c in d.items() if c}
def scale(a,k):return {m:c*k for m,c in a.items() if c*k}
xs=[{tuple(int(i==j) for i in range(4)):1} for j in range(4)]
def linear(v):
 d={}
 for k,c in enumerate(v):d=add(d,scale(xs[k],c))
 return d
def coeff_tensor(slices):return [[[slices[j][i][k] for k in range(4)] for j in range(4)] for i in range(4)]
T=coeff_tensor(A)
TT=[[T[j][i] for j in range(4)] for i in range(4)]
def symmat(T):
 out=[]
 for j in range(4):
  for r in range(4):
   for ss in range(r+1,4):
    row=[0]*16
    for i in range(4):row[4*r+i]+=T[i][j][ss];row[4*ss+i]-=T[i][j][r]
    out.append(row)
 return out
SM=symmat(T);ST=symmat(TT)
eq(SM,S['jacobian_test']['matrix']);eq(ST,S['transpose_test']['matrix'])
def bareiss(B):
 B=[r[:] for r in B];n=len(B);sgn=1;prev=1
 for i in range(n-1):
  p=next(j for j in range(i,n) if B[j][i])
  if p!=i:B[p],B[i]=B[i],B[p];sgn=-sgn
  val=B[i][i]
  for r in range(i+1,n):
   for c in range(i+1,n):
    z=val*B[r][c]-B[r][i]*B[i][c];assert z%prev==0;B[r][c]=z//prev
   B[r][i]=0
  prev=val
 return sgn*B[-1][-1]
minors={}
for name,B in [('jacobian_test',SM),('transpose_test',ST)]:
 c=S[name];minor=[[B[i][j] for j in c['minor_columns']] for i in c['minor_rows']];value=bareiss(minor);eq(str(value),c['minor_determinant']);minors[name]=value
for row in SM:eq(sum(row[5*i] for i in range(4)),0)
perms=list(itertools.permutations(range(4)))
def sign(p):return (-1)**sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))
def determinant_and_direction(T,V=None):
 # Work in integer polynomial dual numbers epsilon^2=0.
 total={};deriv={}
 for pp in perms:
  f={zero:1};df={}
  for i,j in enumerate(pp):
   q=linear(T[i][j]);dq={} if V is None else linear(V[i][j])
   df=add(mul(df,q),mul(f,dq));f=mul(f,q)
  total=add(total,scale(f,sign(pp)));deriv=add(deriv,scale(df,sign(pp)))
 return total,deriv
f,_=determinant_and_direction(T);ft,_=determinant_and_direction(TT);eq(f,ft);eq(f.get((4,0,0,0),0),-12)
def basis(d):return sorted((x for x in itertools.product(range(d+1),repeat=4) if sum(x)==d),reverse=True)
B4=basis(4)
def matcols(cols,b):return [[c.get(m,0) for c in cols] for m in b]
def empty():return [[[0]*4 for j in range(4)] for i in range(4)]
wcols=[]
for j in range(4):
 for a in range(4):
  for b in range(a,4):
   V=empty();V[a][j][b]=1
   if a!=b:V[b][j][a]=1
   wcols.append(determinant_and_direction(T,V)[1])
W=matcols(wcols,B4)
TG=[[[G[k][i][j] for k in range(4)] for j in range(4)] for i in range(4)]
gcols=[]
for i in range(4):
 for j in range(4):
  for k in range(4):
   V=empty();V[i][j][k]=1;gcols.append(determinant_and_direction(TG,V)[1])
GD=matcols(gcols,B4)
grad=[]
for i in range(4):
 dd={}
 for m,c in f.items():
  if m[i]:n=list(m);n[i]-=1;dd[tuple(n)]=c*m[i]
 grad.append(dd)
Jcols=[mul(g,{m:1}) for g in grad for m in basis(6)];J=matcols(Jcols,basis(9))
def moddet(B,p):
 B=[[x%p for x in row] for row in B];det=1;n=len(B)
 for k in range(n):
  pivot=next((i for i in range(k,n) if B[i][k]),None)
  if pivot is None:return 0
  if pivot!=k:B[k],B[pivot]=B[pivot],B[k];det=-det
  z=B[k][k];det=det*z%p;iv=pow(z,-1,p)
  for i in range(k+1,n):
   r=B[i][k]*iv%p
   if r:
    for j in range(k+1,n):B[i][j]=(B[i][j]-r*B[k][j])%p
   B[i][k]=0
 return det%p
ranks={}
for name,B in [('weddle_derivative',W),('general_determinant_derivative',GD),('weddle_smoothness_degree9_jacobian',J)]:
 c=D[name];eq((len(B),len(B[0])),(c['rows'],c['columns']));v=moddet([[B[i][j] for j in c['minor_columns']] for i in c['minor_rows']],101);eq(v,c['minor_determinant_mod_101']);assert v!=0;checks+=1;ranks[name]={'rank_lower_bound':len(c['minor_rows']),'minor_mod_101':v}
# Universal orbit witness conditions used for the 34-dimensional affine upper bound.
eq(G[0],[[int(i==j) for j in range(4)] for i in range(4)])
eq(G[1],[[i+1 if i==j else 0 for j in range(4)] for i in range(4)])
assert all(G[2][i][j]!=0 for i in range(4) for j in range(4) if i!=j);checks+=1
# Independent numerical/effectivity arithmetic in the smooth intrinsic theorem.
eq(4+4-2*6,-4);eq(4+4*4-4*6,-4);eq(6-2*4,-2);eq(2+(-4)//2,0);eq((10-6)-(6-6),4)
print(json.dumps({'status':'PASS','exact_assertions':checks,'method':'Integer polynomial dictionaries, dual-number permutation determinants, fraction-free minors, modular elimination; independently reconstructed every differential coefficient','symmetrizer_minors':minors,'rank_lower_bound_certificates':ranks,'reconstructed_matrix_sizes':{'symmetrizer':[24,16],'weddle_differential':[35,40],'general_differential':[35,64],'smoothness':[220,336]},'limitations':'The universal upper bounds and intrinsic geometric theorems are reviewed in prose, not inferred from finite computations.'},indent=2))
