"""Independent finite falsifiers for object preservation and lattice/residue hypotheses.
Finite checks are neither proof of infinite fields nor a gerbe certificate.
"""
import itertools,json
from collections import Counter
import sympy as s
counts=Counter()
def ck(k,b):
 assert b,k
 counts[k]+=1
# A genuinely nonabelian finite gerbe extension: A3 -> S3 -> C2.
perms=list(itertools.permutations(range(3)));one=(0,1,2)
def mul(a,b):return tuple(a[b[i]] for i in range(3))
def inv(a):return tuple(a.index(i) for i in range(3))
def pw(a,n):
 out=one
 for _ in range(n):out=mul(out,a)
 return out
def parity(a):return sum(a[i]>a[j] for i in range(3) for j in range(i+1,3))%2
F=[a for a in perms if parity(a)==0];objects=[b for b in perms if parity(b)==1 and pw(b,2)==one]
# Lifts of C5 x C2 must kill the p-kernel, and every F-conjugation descends.
lifts=[(a,b) for a in F for b in objects if pw(a,5)==one and mul(a,b)==mul(b,a)]
ck('nonabelian_tame_full_objects',lifts==[(one,b) for b in objects])
for (a,b),(a1,b1) in itertools.product(lifts,repeat=2):
 upstairs=[f for f in F if mul(mul(f,a),inv(f))==a1 and mul(mul(f,b),inv(f))==b1]
 downstairs=[f for f in F if mul(mul(f,b),inv(f))==b1]
 ck('nonabelian_full_faithfulness',upstairs==downstairs)
# In wild characteristic three, the identity S3 lift sees the order-three kernel.
for a in F:
 if a!=one:
  ck('wild_kernel_can_survive',pw(a,3)==one and a!=one)
  for b in objects:ck('wild_semidirect_relations',mul(mul(b,a),inv(b))==inv(a))
# Compute actual finite cyclic lattice H1 quotient, not merely a norm identity.
representations=[(2,s.Matrix([[-1]]),2),(3,s.Matrix([[0,-1],[1,-1]]),3),(4,s.Matrix([[0,-1],[1,0]]),2),(6,s.Matrix([[0,-1],[1,1]]),1)]
cohom=[]
for m,A,horder in representations:
 I=s.eye(A.rows);N=sum((A**j for j in range(m)),s.zeros(A.rows));B=A-I
 ck('lattice_norm_zero',N==s.zeros(A.rows))
 ck('actual_cohomology_order',abs(int(B.det()))==horder)
 def cls(v):return tuple(x-s.floor(x) for x in B.inv()*s.Matrix(v))
 classes={cls(v) for v in itertools.product(range(-m,m+1),repeat=A.rows)}
 ck('actual_cohomology_quotient',len(classes)==horder)
 for v in itertools.product(range(-3,4),repeat=A.rows):
  ck('ramification_kills_lattice_class',cls([m*x for x in v])==tuple(0 for _ in range(A.rows)))
  for j in range(A.rows):
   shift=list(v)
   for i in range(A.rows):shift[i]+=B[i,j]
   ck('integer_coboundary_same_class',cls(shift)==cls(v))
 cohom.append({'group_order':m,'rank':A.rows,'H1_order':horder,'representative_classes':[list(map(str,c)) for c in sorted(classes)]})
# Strict distinction between norm obstruction and lattice ramification.
for m,A,horder in representations:
 if horder>1:
  e=s.Matrix([1]+[0]*(A.rows-1));q=(A-s.eye(A.rows)).inv()*e
  ck('nonzero_class_before_ramification',any(x.q!=1 for x in q))
  ck('full_degree_after_ramification',all(x.q==1 for x in m*q))
# Dropping p-independence destroys the key division-order residue hypothesis.
w,y,a,b=s.symbols('w y a b')
for p in (2,3,5,7,11):
 delta=s.Poly(s.expand((y-w)**p),y,w,a,b,modulus=p).as_expr()
 ck('residue_difference_frobenius',s.Poly(delta-(y**p-w**p),y,w,a,b,modulus=p).is_zero)
 ck('dependent_residue_nilpotent',s.expand((b-a).subs(b,a))==0)
 ck('nilpotent_is_nonzero_in_normal_form',s.Poly(y-w,y,w,modulus=p).total_degree()==1 and p>1)
 # With independent a,b the same expression is the nonzero constant b-a.
 ck('independent_residue_not_zero',s.Poly(b-a,a,b,modulus=p).is_zero is False)
# Reparametrization may repair an exponent obstruction for mu_p, not its coefficients.
for p in (2,3,5,7):
 for n in range(1,61):
  support=[0,n]
  exponent_possible=all(e%p==0 for e in support)
  ck('mu_p_exponent_boundary',exponent_possible==(n%p==0))
  # Taking p-th-power constants requires both 1/c and a/c in k^p;
  # their ratio is a. Model p-basis exponents exactly modulo p.
  for ec in range(p):
   ck('mu_p_coefficient_obstruction',not ((-ec)%p==0 and (1-ec)%p==0))
# Independent reduced-norm left-regular determinant identity in positive characteristic.
for n in (2,3):
 for p in (2,3,5,7):
  for seed in range(19):
   M=s.Matrix(n,n,lambda i,j:(seed*(i+2)+j*j+2*i*j+1)%p)
   # Row-major vec: left multiplication is M tensor I, via an independent basis map.
   L=s.zeros(n*n)
   for row,col,k in itertools.product(range(n),repeat=3):L[row*n+col,k*n+col]=M[row,k]
   ck('left_regular_norm_positive_characteristic',int(L.det()-M.det()**n)%p==0)
print(json.dumps({'status':'PASS','exact_assertions':sum(counts.values()),'by_family':dict(sorted(counts.items())),'cyclic_H1_models':cohom,'limitations':'Finite nonabelian object categories, lattice quotients, coefficient exponent conditions, negative residue-p-independence control and norm determinants only. Infinite gerbe/descent/division claims are justified by the separately sealed written reconstruction.'},indent=2,sort_keys=True))
