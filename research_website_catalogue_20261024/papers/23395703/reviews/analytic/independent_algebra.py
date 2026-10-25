"""Exact own algebra controls; no coordinate calculation is called a gin certificate."""
import sympy as A
import json,math,functools,itertools
x,y,z,w,s,t,u=A.symbols('x y z w s t u');Q=x*y*(x-y)*(x-2*y)*z*w*(x+z+w);polars=[A.diff(Q,v) for v in [x,y,z,w]]
factor_rows=A.Matrix([[A.diff(q,v) for v in [x,y,z,w]] for q in [x,y,x-y,x-2*y,z,w,x+z+w]])
rank2_triples=[c for c in itertools.combinations(range(7),3) if factor_rows[list(c),:].rank()==2]
assert rank2_triples==list(itertools.combinations(range(4),3)) and factor_rows.rank()==4
fs2=[A.Poly(f.subs({x:s,y:t,z:2*s+3*t,w:7*s+11*t},simultaneous=True),s,t).as_expr() for f in polars]
fs3=[A.Poly(f.subs({x:s,y:t,z:u,w:s+2*t+3*u},simultaneous=True),s,t,u).as_expr() for f in polars]
def mons(vs,d):
 if len(vs)==1:return [vs[0]**d]
 return [vs[0]**a*b for a in range(d,-1,-1) for b in mons(vs[1:],d-a)]
def matrix(fs,vs,k):
 mm=mons(vs,k);return A.Matrix([[A.Poly(A.expand(f*m),*vs).coeff_monomial(a) for a in mm] for f in fs for m in mons(vs,k-6)])
def rankmod(M,p):
 a=[[int(v)%p for v in row] for row in M.tolist()];r=0
 for c in range(M.cols):
  pivot=next((i for i in range(r,M.rows) if a[i][c]),None)
  if pivot is None:continue
  a[r],a[pivot]=a[pivot],a[r];q=pow(a[r][c],-1,p);a[r]=[(v*q)%p for v in a[r]]
  for i in range(M.rows):
   if i!=r:
    q=a[i][c];a[i]=[(b-q*v)%p for b,v in zip(a[i],a[r])]
  r+=1
  if r==M.rows:break
 return r
records=[]; matrices={}
for r,k,want in [(3,6,4),(3,7,12),(2,6,4),(2,7,7),(2,8,9)]:
 M=matrix(fs3 if r==3 else fs2,[s,t,u] if r==3 else [s,t],k);rank=M.rank();assert rank==want
 rowids=list(M.T.rref()[1]);colids=list(M.rref()[1]);minor=M.extract(rowids,colids).det();assert minor!=0
 null=M.T.nullspace();assert len(null)==M.rows-rank and all(v.T*M==A.zeros(1,M.cols) for v in null)
 records.append({'section_variables':r,'degree':k,'shape':list(M.shape),'rank':rank,'quotient_dimension':M.cols-rank,'nonzero_minor_rows':rowids,'nonzero_minor_columns':colids,'minor':str(minor),'left_kernel_dimension':len(null)})
 matrices[r,k]=M
assert A.expand(11*s*fs2[0]+11*t*fs2[1]-73*(2*s+3*t)*fs2[2]+25*(7*s+11*t)*fs2[3])==0
# Independently recover a minimal graded syzygy basis and verify its maximal minors.
def as_tuple(v,d):
 mm=mons([s,t],d);return [A.expand(sum(v[j*len(mm)+i]*m for i,m in enumerate(mm))) for j in range(4)]
def flat(v,d):
 return A.Matrix([A.Poly(q,s,t).coeff_monomial(m) for q in v for m in mons([s,t],d)])
syz=[]
for degree in [1,2,3]:
 M=matrix(fs2,[s,t],6+degree);existing=[]
 for j,v in enumerate(syz,1):
  existing.extend(flat([m*q for q in v],degree) for m in mons([s,t],degree-j))
 base=A.Matrix.hstack(*existing) if existing else A.zeros(4*(degree+1),0);oldrank=base.rank()
 for v in M.T.nullspace():
  if base.row_join(v).rank()>oldrank:
   forms=as_tuple(v,degree);den=A.ilcm(*[A.denom(c) for f in forms for c in A.Poly(f,s,t).coeffs()]);forms=[A.expand(den*f) for f in forms];gcd=A.igcd(*[int(c) for f in forms for c in A.Poly(f,s,t).coeffs()]);forms=[f/gcd for f in forms];syz.append(forms);break
 else:raise AssertionError('missingnewsyzygy')
HB=A.Matrix(4,3,lambda i,j:syz[j][i])
signed=[A.expand((-1)**i*HB.extract([j for j in range(4) if j!=i],range(3)).det()) for i in range(4)]
ratios=[A.cancel(a/b) for a,b in zip(signed,fs2)];assert len(set(ratios))==1 and ratios[0]!=0 and not ratios[0].free_symbols
rows=[(1,0),(0,1),(1,-1),(1,-2),(2,3),(7,11),(10,14)];dets=[a*d-b*c for i,(a,b) in enumerate(rows) for c,d in rows[i+1:]];assert len(dets)==21 and all(dets)
badprimes=sorted(set(p for n in dets for p in A.factorint(abs(n))))
assert A.det(A.Matrix([[1,0,0,0],[0,1,0,0],[2,3,1,0],[7,11,3,1]]))==1
assert rankmod(matrices[3,7],7)<12
# Restrict-then-differentiate is demonstrably a different ideal.
Q2=A.expand(Q.subs({x:s,y:t,z:2*s+3*t,w:7*s+11*t},simultaneous=True));Q3=A.expand(Q.subs({x:s,y:t,z:u,w:s+2*t+3*u},simultaneous=True))
wrong2=matrix([A.diff(Q2,v) for v in [s,t]],[s,t],6).rank();wrong3=matrix([A.diff(Q3,v) for v in [s,t,u]],[s,t,u],6).rank();assert wrong2==2 and wrong3==3
hs=[A.expand((1-4*A.Symbol('T')**6+A.Symbol('T')**7+A.Symbol('T')**8+A.Symbol('T')**9)*sum((i+1)*A.Symbol('T')**i for i in range(13))).coeff(A.Symbol('T'),k) for k in range(10)]
assert hs[6:9]==[3,1,0]
print(json.dumps({'status':'own_exact_algebra_passed','matrix_records':records,'rank_two_factor_triples':rank2_triples,'ambient_rank':4,'binary_syzygy_basis':[[str(q) for q in v] for v in syz],'signed_HB_minor_common_ratio':str(ratios[0]),'binary_pair_determinants':dets,'flag_bad_primes_only_not_theorem_characteristics':badprimes,'char7_ternary_degree7_rank':rankmod(matrices[3,7],7),'restrict_then_differentiate_degree6_generator_ranks':[wrong2,wrong3],'binary_Hilbert_values_0_to9':[int(a) for a in hs],'limits':'Finiteexactcontrols, notfullgin/positivecharacteristic/genericity/prioritycertificate.'},indent=2))
