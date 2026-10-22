"""Fresh second-review calculations; no imports of any candidate/audit code.
Exact SymPy expansion, full integer group witnesses, and mixed-characteristic
nonreduced coefficient/ideal tests supplement the independent written proof.
"""
import json,random
from sympy import Matrix,eye,symbols,expand
checks={}
def need(v,label):
 if not v:raise RuntimeError(label)
 checks[label]=True
X,Y,Z=symbols('X Y Z',commutative=False)
br=lambda a,b:a*b-b*a
P=expand(br(br(br(X,Y),br(X,Z)),X));Q=expand(br(br(br(X,Y),br(X,br(X,Y))),X))
need(P.coeff(X*X*Y*X*Z)==-1,'free_associative_decisive_coefficient_minus1')
need(Q.coeff(X*X*X*Y*X*Y)==1,'weighted_free_associative_decisive_coefficient_plus1')
need(len(P.args)==12 and len(Q.args)==10,'free_polynomial_full_term_counts')
# Full untruncated words in integer unitriangular groups, using exact rational
# inverse from SymPy rather than a Magnus expansion or colored-path code.
def gc(a,b):return a*b*a.inv()*b.inv()
def w(m):x,y,z=m;return gc(gc(gc(x,y),gc(x,z)),x)
def v(m):x,y=m;return gc(gc(gc(x,y),gc(x,gc(x,y))),x)
def unipotent(n,edges):
 a=eye(n)
 for i,j in edges:a[i-1,j-1]=1
 return a
m=[unipotent(6,[(1,2),(2,3),(4,5)]),unipotent(6,[(3,4)]),unipotent(6,[(5,6)])]
e=eye(6);e[0,5]=-1
need(w(m)==e,'full_integer_UT6_word_is_I_minus_E16')
m=[unipotent(7,[(1,2),(2,3),(3,4),(5,6)]),unipotent(7,[(4,5),(6,7)])]
e=eye(7);e[0,6]=1
need(v(m)==e,'full_integer_UT7_word_is_I_plus_E17')
# Actual finite ideal powers in Z/59049; (3)^r remains nonzero through r=9.
MOD=59049
ident=(1,0,0,1)
def mm(a,b):return tuple(sum(a[2*i+k]*b[2*k+j]for k in range(2))%MOD for i in range(2)for j in range(2))
def mi(a):return(a[3],-a[1]%MOD,-a[2]%MOD,a[0])
def cc(a,b):return mm(mm(mm(a,b),mi(a)),mi(b))
def mat(a,b,c):
 a,b,c=3*a%MOD,3*b%MOD,3*c%MOD
 return((1+a)%MOD,b,c,(1+b*c)*pow(1+a,-1,MOD)%MOD)
observations={'w_next_degree_nonzero':0,'v_next_degree_nonzero':0,'deleted_outer_insufficient':0}
rng=random.Random(68130003703)
for j in range(1,193):
 x,y,z=(mat(*(rng.randrange(1000)for k in range(3)))for k in range(3))
 for a in(x,y,z):
  if (a[0]*a[3]-a[1]*a[2])%MOD!=1:raise RuntimeError('det')
 u=cc(x,y);ww=cc(cc(u,cc(x,z)),x);vv=cc(cc(u,cc(x,u)),x)
 dw=tuple((a-b)%MOD for a,b in zip(ww,ident));dv=tuple((a-b)%MOD for a,b in zip(vv,ident))
 if any(a%729 for a in dw)or any(a%2187 for a in dv):raise RuntimeError('actual ideal bound')
 observations['w_next_degree_nonzero']+=any(a%2187 for a in dw)
 observations['v_next_degree_nonzero']+=any(a%6561 for a in dv)
 inner=cc(u,cc(x,z));observations['deleted_outer_insufficient']+=any((a-b)%729 for a,b in zip(inner,ident))
need(all(observations.values()),'192_full_SL2_words_over_Z59049_actual_ideal_bounds_and_strict_next_terms')
# P over the nonreduced commutative ring Z/6[u,v]/(u^2,v^2), using 4-tuples.
def plus(a,b,sign=1):return tuple((x+sign*y)%6 for x,y in zip(a,b))
def times(a,b):
 c=[0]*4
 for i,x in enumerate(a):
  for k,y in enumerate(b):
   if not i&k:c[i|k]=(c[i|k]+x*y)%6
 return tuple(c)
zero=(0,0,0,0)
def rm(a,b):return tuple(tuple(plus(times(a[i][0],b[0][j]),times(a[i][1],b[1][j]))for j in range(2))for i in range(2))
def rb(a,b):
 c,d=rm(a,b),rm(b,a)
 return tuple(tuple(plus(c[i][j],d[i][j],-1)for j in range(2))for i in range(2))
def gen(rng):return tuple(tuple(tuple(rng.randrange(6)for k in range(4))for j in range(2))for i in range(2))
ring_rng=random.Random(68115987013);seen=set()
for i in range(1,193):
 a,b,c=gen(ring_rng),gen(ring_rng),gen(ring_rng);seen.add((a,b,c))
 if rb(rb(rb(a,b),rb(a,c)),a)!=((zero,zero),(zero,zero)):raise RuntimeError('nonreduced P')
need(len(seen)==192,'192_distinct_arbitrary_matrix_triples_over_Z6_dual_two_variable_ring')
print(json.dumps({'schema':'pr681-round2-math-controls-v1','status':'PASS','checks':checks,'count':len(checks),'mixed_characteristic_ideal_samples':192,'nonreduced_ring_triples':192,'ideal_observations':observations,'source_code_imported':False,'role':'Exact finite corroboration; universal deductions supplied in DERIVATION.md'},indent=2,sort_keys=True))
