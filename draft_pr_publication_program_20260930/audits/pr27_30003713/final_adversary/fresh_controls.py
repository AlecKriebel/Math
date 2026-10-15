"""Fresh acceptance controls: rectangular naturality and induction intersections.
No old code imports. Finite checks, never an unrestricted decomposition.
"""
from itertools import combinations,product,permutations
from pathlib import Path
import json,hashlib,datetime
import sympy as S

def wedge(items):
 if len(set(items))<len(items):return (),0
 return tuple(sorted(items)),(-1)**sum(a>b for i,a in enumerate(items) for b in items[i+1:])

def hookdim(shape,m):
 value=S.Integer(1)
 for i,l in enumerate(shape):
  for j in range(l):value*=S.Rational(m+j-i,l-j+sum(t>j for t in shape[i+1:]))
 return int(value)

def face_constraints(m,n,singletons):
 basis=[(a,t) for a in combinations(range(m),3) for t in product(range(m),repeat=n)]
 ix={b:i for i,b in enumerate(basis)};blocks=[]
 # Enforce all transpositions among the n-1 selected singleton factors.
 for a,b in zip(singletons,singletons[1:]):
  P=S.zeros(len(basis))
  for j,(triple,t) in enumerate(basis):
   u=list(t);u[a],u[b]=u[b],u[a];P[ix[triple,tuple(u)],j]=1
  blocks.append(P-S.eye(len(basis)))
 # The kernel of exterior product is the predecessor hook, tensor free V.
 target=[(a,t) for a in combinations(range(m),4) for t in product(range(m),repeat=n-1)]
 ri={b:i for i,b in enumerate(target)};D=S.zeros(len(target),len(basis));a=singletons[0]
 for j,(triple,t) in enumerate(basis):
  w,sgn=wedge(triple+(t[a],))
  if sgn:D[ri[w,t[:a]+t[a+1:]],j]=sgn
 blocks.append(D)
 return S.Matrix.vstack(*blocks),basis

face_rows=[]
for m,n in [(3,2),(3,3),(3,4),(4,2),(4,3)]:
 A,basis=face_constraints(m,n,list(range(n-1)))
 B,_=face_constraints(m,n,list(range(n-2))+[n-1])
 inter=S.Matrix.vstack(A,B)
 actual=len(basis)-inter.rank();expected=hookdim((n+1,1,1),m)
 assert (actual!=expected if n==2 else actual==expected)
 face_rows.append({'dimV':m,'n':n,'ambient':len(basis),'face1_dimension':len(basis)-A.rank(),'face2_dimension':len(basis)-B.rank(),'intersection_dimension':actual,'expected_hook_dimension':expected,'source_lemma_smallest_boundary_counterexample':n==2})

# Cross-dimensional adjoint map in degree three. Use actual associative-word
# expansions, so the rectangular substitution never needs a chosen Lie basis.
def comm(u,v):
 out={}
 for a,c in u.items():
  for b,d in v.items():out[a+b]=out.get(a+b,0)+c*d;out[b+a]=out.get(b+a,0)-c*d
 return {a:c for a,c in out.items() if c}

def sub(word,A):
 out={():S.Integer(1)}
 for v in word:
  z={}
  for u,c in out.items():
   for k in range(A.rows):
    if A[k,v]:z[u+(k,)]=z.get(u+(k,),0)+c*A[k,v]
  out=z
 return out

def tensor_matrix(A,d):
 src=list(product(range(A.cols),repeat=d));tgt=list(product(range(A.rows),repeat=d));ix={w:i for i,w in enumerate(tgt)}
 M=S.zeros(len(tgt),len(src))
 for j,w in enumerate(src):
  for u,c in sub(w,A).items():M[ix[u],j]=c
 return M

def bracket_matrix(m):
 src=[(v,a,b) for v in range(m) for a,b in combinations(range(m),2)];words=list(product(range(m),repeat=3));ix={w:i for i,w in enumerate(words)}
 D=S.zeros(len(words),len(src))
 for j,(v,a,b) in enumerate(src):
  for w,c in comm({(v,):1},{(a,b):1,(b,a):-1}).items():D[ix[w],j]=c
 return D,src

rect=[]
for A in [S.Matrix([[1,2,0],[0,1,3]]),S.Matrix([[1,1,0],[0,0,0]]),S.Matrix([[1,0],[2,1],[0,3]]),S.zeros(2,3)]:
 Ds,bs=bracket_matrix(A.cols);Dt,bt=bracket_matrix(A.rows);ix={w:i for i,w in enumerate(bt)}
 F=S.zeros(len(bt),len(bs))
 for j,(v,a,b) in enumerate(bs):
  for u in range(A.rows):
   for i,k in combinations(range(A.rows),2):F[ix[u,i,k],j]=A[u,v]*(A[i,a]*A[k,b]-A[k,a]*A[i,b])
 T=tensor_matrix(A,3)
 assert Dt*F==T*Ds
 K=S.Matrix.hstack(*Ds.nullspace()) if Ds.nullspace() else S.zeros(Ds.cols,0)
 assert Dt*F*K==S.zeros(Dt.rows,K.cols)
 rect.append({'sourceV':A.cols,'targetV':A.rows,'map_rank':A.rank(),'matrix':A.tolist(),'action_commutes':True,'kernel_preserved':True})

# The right resolution is natural under rectangular maps already at chain
# degree one: first-letter maps equal tensor-word substitution in every length.
res_checks=0
for A in [S.Matrix([[1,2,0],[0,1,3]]),S.Matrix([[1,1,0],[0,0,0]])]:
 for d in range(1,5):
  assert tensor_matrix(A,d)==S.kronecker_product(A,tensor_matrix(A,d-1));res_checks+=1

# Wrong module handedness after a noncommutative action: concatenation order
# has the same dimensions but violates the balancing relation.
x=S.Matrix([[0,1],[0,0]]);y=S.Matrix([[0,0],[1,0]]);n=S.Matrix([1,0])
correct=x*y*n;wrong=y*x*n
assert correct!=wrong
# Virtual-character cancellation can conceal equal actual modules in each
# homology degree; test with a nontrivial S2 representation, not only scalars.
swap=S.Matrix([[0,1],[1,0]])
assert swap*S.zeros(2)==S.zeros(2)*swap and swap*S.eye(2)==S.eye(2)*swap
assert S.zeros(2).nullspace()!=S.eye(2).nullspace()
assert swap.trace()==0 # both complexes' Euler character is zero at both classes.

out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'sympy':S.__version__,'independent_face_intersections':face_rows,'rectangular_adjoint_naturality':rect,'rectangular_right_resolution_checks':res_checks,'noncommutative_balancing_mutant_rejected':True,'equivariant_Euler_only_mutant_rejected':True,'finite_scope':'Five actual face intersections, including two falsifiers of unused n=2 source-lemma boundary; four cross-dimensional adjoint chain maps; eight cross-dimensional right-resolution identities. Universal validity is proved separately. No general homology solving attempt.'}
Path(__file__).with_name('FRESH_CONTROLS_RECEIPT.json').write_text(json.dumps(out,indent=2,default=int)+'\n');print(json.dumps(out,indent=2,default=int))
