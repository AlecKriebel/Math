"""Own exact controls for the cubic subclass; no external executable inputs."""
from itertools import combinations,product
from collections import Counter
import sympy as s
import json
C=Counter()
def ck(v,key):
 assert v,key
 C[key]+=1
Q,F,G,S,T,d,e,f,g=s.symbols('Q F G S T d e f g',nonzero=True)
expr=lambda x: Q*x*(F-S-x)-(G-T-1/x)
ck(s.simplify(expr(d)-expr(e)-(d-e)*(Q*(F-S-d-e)-1/(d*e)))==0,'reflection_difference')
base=lambda x,y:x+y+1/(Q*x*y)
ck(s.factor(base(d,e)-base(d,f))==(e-f)*(Q*d*e*f-1)/(Q*d*e*f),'three_value_factor')
u=s.symbols('u');a=s.symbols('a:6')
def quad(x,y,z):return a[0]*x*x+a[1]*y*y+a[2]*z*z+a[3]*x*y+a[4]*x*z+a[5]*y*z
node=[u*u,u,-(u**3+1)];cusp=[u,1,u**3]
ck(s.expand(node[0]*node[1]*node[2]+node[0]**3+node[1]**3)==0,'nodal_equation')
ck(s.expand(cusp[1]**2*cusp[2]-cusp[0]**3)==0,'cuspidal_equation')
N=s.Poly(quad(*node),u);K=s.Poly(quad(*cusp),u)
ck(N.nth(0)==N.nth(6)==a[2],'nodal_product_law')
ck(K.nth(5)==0 and K.nth(6)==a[2],'cuspidal_sum_law')
# Exact residual obstruction for every 7-, 8-, and 9-point subset of E[3].
E=list(product(range(3),repeat=2)); witness_count=0
for n in [7,8,9]:
 for A in combinations(E,n):
  P=set(A);found=False
  for B in combinations(A,5):
   r=tuple(-sum(p[j] for p in B)%3 for j in range(2))
   if r not in P or r in B:found=True;break
  ck(found,'all_large_E3_subsets_have_residual_witness');witness_count+=1
# No five-subset loop here assumes that different parameters are different points.
for name,par in [('node',node),('cusp',cusp)]:
 vals=list(range(1,10))
 pts=[tuple(s.sympify(v).subs(u,t) for v in par) for t in vals]
 ck(len({tuple(s.Rational(v)/next(x for x in p if x) for v in p) for p in pts})==9,'distinct_parametric_points')
 V=s.Matrix([[x*x,y*y,z*z,x*y,x*z,y*z] for x,y,z in pts]);ck(V.rank()==6,'not_on_conic')
 ordinary=0
 for ids in combinations(range(9),5):
  M=V[list(ids),:];ck(M.rank()==5,'five_point_uniqueness')
  coeff=M.nullspace()[0];support=[j for j in range(9) if (V[j,:]*coeff)[0]==0]
  if len(support)==5:ordinary+=1
 ck(ordinary>0,'actual_ordinary_conic_on_singular_cubic')
 # Every six coconic smooth parameters obeys the appropriate residual law.
 for ids in combinations(range(9),6):
  if V[list(ids),:].det()==0:
   ck(s.prod(vals[j] for j in ids)==1 if name=='node' else sum(vals[j] for j in ids)==0,'six_point_residual_law')
# Literal character injection on finite coordinate boxes: rationals and roots
# represented by a prime-power rational and separate modular coordinates.
seen=set()
for k,l,a0,b0 in product(range(-2,3),range(-2,3),range(3),range(4)):
 key=(s.Rational(2)**k*s.Rational(3)**l,a0,b0)
 ck(key not in seen,'two_character_injection_control');seen.add(key)
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(C),'E3_subsets_checked':witness_count,'scope':'Finite controls only; universal reflection and cubic theorem are proved in TURN_4.md.'},indent=2,sort_keys=True))
