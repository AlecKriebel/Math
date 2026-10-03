#!/usr/bin/env python3
"""Portable independent mathematical audit. No author verifier imported.
Generate quaternion group from two generators and identify with SL2(F5),
construct SL2(F4) modules, recheck the published A5 idempotents, and derive
characters/PIM data. Writes only its result JSON beside this script.
"""
from fractions import Fraction as Q
from collections import Counter, deque
from itertools import product, permutations
from pathlib import Path
import re,json,hashlib
import sympy as sp
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent

# Independent quadratic-field and quaternion arithmetic, phi^2=phi+1.
def add(x,y):return (x[0]+y[0],x[1]+y[1])
def neg(x):return (-x[0],-x[1])
def mul(x,y):return (x[0]*y[0]+x[1]*y[1],x[0]*y[1]+x[1]*y[0]+x[1]*y[1])
def scale(x,n):return(x[0]*n,x[1]*n)
def sm(xs):
 r=(Q(0),Q(0))
 for x in xs:r=add(r,x)
 return r
z=(Q(0),Q(0));o=(Q(1),Q(0));ph=(Q(0),Q(1));half=Q(1,2)
def qm(x,y):
 s=add(mul(x[0],y[0]),neg(sm(mul(x[i],y[i]) for i in (1,2,3))))
 v=[]
 for i,j,k in [(1,2,3),(2,3,1),(3,1,2)]:
  v.append(sm([mul(x[0],y[i]),mul(y[0],x[i]),mul(x[j],y[k]),neg(mul(x[k],y[j]))]))
 return(s,*v)
qe=(o,z,z,z);qa=(z,o,z,z);qb=(scale(o,half),scale(ph,-half),scale(add(ph,neg(o)),half),z)
def mm5(a,b):return tuple(sum(a[2*i+k]*b[2*k+j] for k in range(2))%5 for i in range(2) for j in range(2))
me=(1,0,0,1);ma=(0,1,4,0);mb=(0,1,4,1)
# Simultaneous Cayley graphs prove a bijective group homomorphism.
q_to_m={qe:me};todo=deque([qe]);max_seen=0
while todo:
 q=todo.popleft()
 for u,v in [(qa,ma),(qb,mb)]:
  q1=qm(q,u);m1=mm5(q_to_m[q],v)
  if q1 in q_to_m:assert q_to_m[q1]==m1
  else:
   q_to_m[q1]=m1;todo.append(q1)
   assert len(q_to_m)<=120
assert len(q_to_m)==len(set(q_to_m.values()))==120
SL5={x for x in product(range(5),repeat=4) if (x[0]*x[3]-x[1]*x[2])%5==1}
assert set(q_to_m.values())==SL5
for q in q_to_m:
 assert sm(mul(t,t) for t in q)==o
 for r in q_to_m:assert q_to_m[qm(q,r)]==mm5(q_to_m[q],q_to_m[r])
def order(g,mult,ident):
 h=ident
 for n in range(1,121):
  h=mult(h,g)
  if h==ident:return n
 raise AssertionError('order bound')
qo={q:order(q,qm,qe) for q in q_to_m}
def symcube(q):
 t=scale(q[0],2);u=add(mul(mul(t,t),t),scale(t,-2));assert u[1]==0
 return u[0]
cm={q:symcube(q) for q in q_to_m}
assert sum(v*v for v in cm.values())==120
assert sum(symcube(qm(q,q)) for q in q_to_m)==-120
cp={q:{1:4,2:4,3:1,4:0,5:-1,6:1,10:-1}[qo[q]] for q in q_to_m}
assert sum(cp[q]*cm[q] for q in q_to_m)==0
assert sum(cp[q]**2 for q in q_to_m)==120
psi={q:2*cp[q] if qo[q]%2 else Q(0) for q in q_to_m}
assert all(psi[q]==cp[q]+cm[q] for q in q_to_m)
assert sum(psi[q]*cm[q] for q in q_to_m)==120

# Construct the quotient's five-point action by conjugation on its Sylow 2s.
def inv5(m):return (m[3],(-m[1])%5,(-m[2])%5,m[0])
mo={m:order(m,mm5,me) for m in SL5}
zm=(4,0,0,4)
Q8s=set()
for x in SL5:
 if mo[x]!=4:continue
 for y in SL5:
  if mo[y]!=4 or mo[mm5(x,y)]!=4:continue
  cur={me};queue=[me]
  for h in queue:
   for gen in (x,y):
    nxt=mm5(h,gen)
    if nxt not in cur:cur.add(nxt);queue.append(nxt)
  if len(cur)==8:Q8s.add(frozenset(cur))
assert len(Q8s)==5
Q8s=list(Q8s)
paction={}
for g in SL5:
 paction[g]=tuple(Q8s.index(frozenset(mm5(mm5(g,x),inv5(g)) for x in P)) for P in Q8s)
assert len(set(paction.values()))==60
assert all(sum(a>b for i,a in enumerate(paction[g]) for b in paction[g][i+1:])%2==0 for g in SL5)
assert {g for g in SL5 if paction[g]==tuple(range(5))}=={me,zm}
assert all(cp[q]==sum(i==v for i,v in enumerate(paction[q_to_m[q]]))-1 for q in qo)
# All nine actual irreducibles from Sym^0,...,Sym^5, conjugation, augmentation.
def symchar(t,n):
 u,v=o,t
 if n==0:return u
 for _ in range(1,n):u,v=v,add(mul(t,v),neg(u))
 return v
def gal(t):return(t[0]+t[1],-t[1])
labels=['1','2a','2b','3a','3b','4+','4-','5','6']
chars={}
for q in qo:
 t=scale(q[0],2)
 chars[q]=[o,t,gal(t),symchar(t,2),gal(symchar(t,2)),(cp[q],Q(0)),symchar(t,3),symchar(t,4),symchar(t,5)]
for i,j in product(range(9),repeat=2):
 assert sm(mul(chars[q][i],chars[q][j]) for q in qo)==(Q(120 if i==j else 0),Q(0))
indicators=[]
for i in range(9):
 value=scale(sm(chars[qm(q,q)][i] for q in qo),Q(1,120));assert value[1]==0
 indicators.append(int(value[0]))
assert indicators==[1,-1,-1,1,1,1,-1,1,-1]
assert sum(int(x[0])**2 for x in chars[qe])==120

# F4 = F2[a]/(a^2+a+1), encoded by two bits.
def fmul(a,b):
 r=0
 for i in range(2):
  if (b>>i)&1:r^=a<<i
 if r&4:r^=7
 return r
finv={1:1,2:3,3:2}
def mm4(a,b):return tuple(fmul(a[2*i],b[j])^fmul(a[2*i+1],b[2+j]) for i in range(2) for j in range(2))
H=[x for x in product(range(4),repeat=4) if fmul(x[0],x[3])^fmul(x[1],x[2])==1]
assert len(H)==60
he=(1,0,0,1)
def frank(rows):
 rows=[list(x) for x in rows];r=0
 for col in range(len(rows[0])):
  at=next((i for i in range(r,len(rows)) if rows[i][col]),None)
  if at is None:continue
  rows[r],rows[at]=rows[at],rows[r];u=finv[rows[r][col]]
  rows[r]=[fmul(v,u) for v in rows[r]]
  for j in range(len(rows)):
   if j!=r and rows[j][col]:
    v=rows[j][col];rows[j]=[x^fmul(v,y) for x,y in zip(rows[j],rows[r])]
  r+=1
 return r
def rank2(rows):
 piv={}
 for row in rows:
  while row:
   i=row.bit_length()-1
   if i in piv:row^=piv[i]
   else:piv[i]=row;break
 return len(piv)
assert frank(H)==4
T=[]
for g in H:
 T.append(tuple(fmul(g[2*i+j],fmul(g[2*k+l],g[2*k+l])) for i,k in product(range(2),repeat=2) for j,l in product(range(2),repeat=2)))
assert frank(T)==16
# Restriction of scalars natural 2-dimensional F4 module to F2^4.
U=[]
for g in H:
 cols=[]
 for j,b in product(range(2),range(2)):
  coeff=1<<b;cols.append(sum(fmul(g[2*i+j],coeff)<<(2*i) for i in range(2)))
 U.append(sum(((cols[j]>>i)&1)<<(4*i+j) for i,j in product(range(4),repeat=2)))
assert rank2(U)==8
# Projective line action identifies SL2(F4) with the entire alternating group.
points=[(1,0)]+[(a,1) for a in range(4)]
def pnorm(v):
 a,b=v
 if b==0:return(1,0)
 return(fmul(a,finv[b]),1)
perms={}
for g in H:
 perms[g]=tuple(points.index(pnorm((fmul(g[0],v[0])^fmul(g[1],v[1]),fmul(g[2],v[0])^fmul(g[3],v[1])))) for v in points)
assert len(set(perms.values()))==60
assert all(sum(p[i]>p[j] for i in range(5) for j in range(i+1,5))%2==0 for p in perms.values())
# Explicit F2 augmentation module S on five points.
S=[]
for g in H:
 p=perms[g];S.append(sum(((int(p[j]==i)^int(p[4]==i)))<<(4*i+j) for i,j in product(range(4),repeat=2)))
assert rank2(S)==16
ho={g:order(g,mm4,he) for g in H}
# Character classes of the four simple F4 modules follow from eigenvalue lifts.
p=(1+sp.sqrt(5))/2
B=sp.Matrix([[1,1,1,1],[2,-1,p-1,-p],[2,-1,-p,p-1],[4,1,-1,-1]])
Gram=(B*sp.diag(1,20,12,12)*B.T/60).applyfunc(sp.simplify)
Cartan=Gram.inv().applyfunc(sp.simplify)
assert Cartan==sp.Matrix([[4,2,2,0],[2,2,1,0],[2,1,2,0],[0,0,0,1]])

# Independently multiply the explicitly listed mathematical idempotents.
# Coefficients are from Johnston--Rumynin Table 5, with source cited in JSON.
def pm(a,b):return tuple(a[b[i]] for i in range(5))
def pi(a):return tuple(a.index(i) for i in range(5))
input_data=json.loads((HERE/'a5_idempotents.json').read_text())
entries=[(tuple(e['permutation']),[Q(x) for x in e['coefficients']]) for e in input_data['entries']]
assert len(entries)==len(set(x[0] for x in entries))==60
AG=sorted(perms.values());ae=tuple(range(5));idx={g:i for i,g in enumerate(AG)}
Es=[{g:c[j] for g,c in entries} for j in range(3)]
idempotent_report=[]
perm_to_h={v:k for k,v in perms.items()}
for ej in Es:
 assert all(c.denominator%2 for c in ej.values())
 squared={g:Q(0) for g in AG}
 for g,h in product(AG,repeat=2):squared[pm(g,h)]+=ej[g]*ej[h]
 assert squared==ej
 # Rank of the reduced right-multiplication matrix gives Ae dimension.
 ebar={g:int(c.numerator%2) for g,c in ej.items()}
 rank=rank2([sum(ebar[h]<<idx[pm(g,h)] for h in AG) for g in AG])
 char={g:sum(ej[pm(pm(pi(x),pi(g)),x)] for x in AG) for g in AG}
 assert char[ae]==rank
 # Each idempotent's images on the split simple modules identify its top.
 natural=[0]*4;tensor=[0]*16
 for g in AG:
  if not ebar[g]:continue
  mat=perm_to_h[g]
  for i in range(4):natural[i]^=mat[i]
  tm=T[H.index(mat)]
  for i in range(16):tensor[i]^=tm[i]
 topranks=[sum(ebar.values())%2,frank([natural[:2],natural[2:]]),frank([tensor[i:i+4] for i in range(0,16,4)])]
 rows={n:sorted({char[perms[g]] for g in H if ho[g]==n}) for n in sorted(set(ho.values()))}
 idempotent_report.append({'rank_F2':rank,'top_ranks_1_N_S':topranks,'ordinary_character_by_order':{str(k):[str(x) for x in v] for k,v in rows.items()}})
assert [r['rank_F2'] for r in idempotent_report]==[12,16,4]
assert [r['top_ranks_1_N_S'] for r in idempotent_report]==[[1,0,0],[0,1,0],[0,0,1]]
smallB=sp.Matrix([[1,1,1],[4,-2,-1],[4,1,-1]])
Prows=sp.Matrix([[12,0,2],[16,-2,1],[4,1,-1]])
F2C=Prows*smallB.inv()
assert F2C==sp.Matrix([[4,2,0],[4,3,0],[0,0,1]])

# Explicitly lift each modular idempotent through the central square-zero ideal.
# In characteristic 2, if a^2-a is square-zero then a^2 is idempotent.
GG=sorted(SL5);gi={g:i for i,g in enumerate(GG)}
section={}
for g in GG:section.setdefault(paction[g],g)
assert len(section)==60
prodindex=[[gi[mm5(g,h)] for h in GG] for g in GG]
def support(bits):
 while bits:
  b=bits&-bits;yield b.bit_length()-1;bits^=b
def gamul(a,b):
 r=0
 for i in support(a):
  for j in support(b):r^=1<<prodindex[i][j]
 return r
def left_translate(i,b):
 r=0
 for j in support(b):r^=1<<prodindex[i][j]
 return r
central_projectives=[]
for ej in Es:
 a=sum(1<<gi[section[g]] for g,c in ej.items() if c.numerator%2)
 e=gamul(a,a);assert gamul(e,e)==e
 P=[left_translate(i,e) for i in range(120)]
 tP=[v^left_translate(gi[zm],v) for v in P]
 dim=rank2(P);trank=rank2(tP);assert dim==2*trank
 central_projectives.append({'dimension':dim,'central_z_minus_1_rank':trank,'central_z_minus_1_kernel_dimension':dim-trank})
assert [x['dimension'] for x in central_projectives]==[24,32,8]
assert [x['central_z_minus_1_rank'] for x in central_projectives]==[12,16,4]
# The inflated 8-dimensional witness 2V4 has central rank 0; genuine PIM8 has rank 4.

# Rational witnesses are augmentation representations on 5 and 6 points.
# Six-point action of SL2(F5) descends to its central quotient.
p5=[(1,0)]+[(a,1) for a in range(5)]
def normalize5(v):
 a,b=v
 if b==0:return(1,0)
 return(a*pow(b,-1,5)%5,1)
chi5={m:sum(normalize5(((m[0]*a+m[1]*b)%5,(m[2]*a+m[3]*b)%5))==(a,b) for a,b in p5)-1 for m in SL5}
assert sum(v*v for v in chi5.values())==120
assert all(chi5[q_to_m[q]]=={1:5,2:5,3:-1,4:1,5:0,6:-1,10:0}[qo[q]] for q in qo)
assert (sp.Matrix([[5,-1,0]])*smallB.inv())==sp.Matrix([[1,1,0]])
assert (sp.Matrix([[4,1,-1]])*smallB.inv())==sp.Matrix([[0,0,1]])
# Core results and the unchanged audited mathematical proof.
proof_hash=hashlib.sha256((ROOT/'COUNTEREXAMPLE.md').read_bytes()).hexdigest()
assert proof_hash=='3ceab2f387baa3d61c15805cdde7d8154c8350e2b3b4bf2ce187ec53b99ec299'
result={
 'proof_sha256':proof_hash,
 'quaternion_SL2F5_bijection':len(q_to_m),'all_homomorphism_products_checked':14400,
 'element_order_counts':dict(sorted(Counter(qo.values()).items())),
 'quotient_Sylow2_permutation_action_kernel_order':2,'all_nine_actual_character_orthogonality':True,'ordinary_labels':labels,'all_FS_indicators':indicators,
 'faithful_Sym3_norm':1,'faithful_Sym3_FS':-1,'degree4_inner_product':0,'forced_projective_faithful_multiplicity':1,
 'SL2F4_order':len(H),'projective_line_identifies_A5':True,
 'natural_matrix_span_over_F4':4,'tensor_matrix_span_over_F4':16,'underlying_natural_matrix_span_over_F2':8,'augmentation_matrix_span_over_F2':16,
 'A5_Cartan_over_F4':Cartan.tolist(),'A5_F2_PIM_composition_rows':F2C.tolist(),
 'source_Table5_idempotents':idempotent_report,
 'explicit_SL2F5_modular_projectives':central_projectives,
 'SL2F5_F2_PIM_composition_rows':(2*F2C).tolist(),
 'rational_degree5_augmentation_norm':1,
 'all_checks_passed':True}
(HERE/'independent_results.json').write_text(json.dumps(result,indent=2,default=str)+'\n')
print(json.dumps(result,indent=2,default=str))
