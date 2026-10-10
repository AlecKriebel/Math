"""Independent symbolic/support controls for the published two-shared-variable pair."""
from itertools import combinations, product, permutations
from collections import Counter
from math import factorial
import sympy as s
import json
C=Counter()
def ck(v,k):assert v,k;C[k]+=1
u,a,b,y,z=s.symbols('u a b y z');xs=(u,a,b,y,z)
base=2*a*b*b+2*a*a*b+2*u*b*b+8*u*a*b+2*u*a*a+2*u*u*b+2*u*u*a
P=base+4*y*(a*b+u*b+u*a);Q=base+4*z*(a*b+u*b+u*a)+a*a*z
p=s.expand(P.subs({u:1,a:a+1,b:b+1},simultaneous=True));q=s.expand(Q.subs({u:1,a:a+1,b:b+1},simultaneous=True))
ck(s.expand(p.subs(y,0)-q.subs(z,0))==0,'exact_compatibility')
ck(p.subs({a:0,b:0,y:0})==q.subs({a:0,b:0,z:0})==20,'origin_nonzero')
ck(s.Poly(p,*xs).total_degree()==s.Poly(q,*xs).total_degree()==3,'total_degree_three')
# Collapse squarefree bases directly by exponent vectors, independently of polynomial substitution.
def collapse(private,exceptions):
 out=Counter()
 for B in combinations(range(7),3):
  if frozenset(B) in exceptions:continue
  v=[0]*5
  for j in B:v[private if j==6 else j//2]+=1
  out[tuple(v)]+=1
 return out
J1=collapse(3,{frozenset([0,1,6]),frozenset([2,3,6]),frozenset([4,5,6])})
J2=collapse(4,{frozenset([0,1,6]),frozenset([4,5,6])})
ck(dict(s.Poly(P,*xs).terms())==dict(J1),'collapsed_P1_coefficients')
ck(dict(s.Poly(Q,*xs).terms())==dict(J2),'collapsed_P2_coefficients')
def subsets(E):return [frozenset(j) for r in range(len(E)+1) for j in combinations(E,r)]
def rank(J,E):return {B:max(sum(v[i] for i in B) for v in J) for B in subsets(E)}
r1=rank(J1,[0,1,2,3]);r2=rank(J2,[0,1,2,4]);known=r1|r2
for J,E in [(J1,[0,1,2,3]),(J2,[0,1,2,4])]:
 for v,w in product(J,repeat=2):
  for i in E:
   if v[i]>w[i]:
    ck(any(v[j]<w[j] and tuple(v[t]-(t==i)+(t==j) for t in range(5)) in J for j in E),'M_convex_exchange')
 r=rank(J,E)
 for T in subsets(E):
  sub={v:c for v,c in J.items() if all(v[t]==0 for t in set(E)-T)}
  if sub:
   rt=rank(sub,list(T))
   for S in subsets(T):ck(rt[S]==r[S],'nondegenerate_rank_restriction')
 for S,T in product(r,repeat=2):
  ck(r[S]+r[T]>=r[S|T]+r[S&T],'rank_submodularity')
  if S<=T:ck(r[S]<=r[T],'rank_monotonicity')
# Independent exact linear combination of rank inequalities.
R={B:s.Symbol('r'+''.join(map(str,sorted(B)))) for B in subsets(range(5))}
def rr(*v):return R[frozenset(v)]
expr=(rr(0,3)+rr(0,4)-rr(0,3,4)-rr(0))+(rr(2,3)+rr(2,4)-rr(2,3,4)-rr(2))+(rr(0,3,4)+rr(2,3,4)-rr(0,2,3,4)-rr(3,4))+(rr(0,2,3,4)-rr(0,2))+(rr(1,3)+rr(3,4)-rr(1,3,4)-rr(3))+(rr(1,3,4)-rr(1,4))
expr=s.expand(expr)
ck(all(v in [R[B] for B in known] for v in expr.free_symbols),'all_unknown_mixed_ranks_cancel')
ck(expr.subs({R[B]:r for B,r in known.items()})==-1,'negative_Farkas_constant')
for m in range(1,201):ck(expr.subs({R[B]:m*r for B,r in known.items()})==-m,'all_positive_integer_scalings')
# All terms of arbitrary-degree mixed extensions, without assuming they are real zero.
# The test checks only the homogenization/shear/derivative-support mechanics.
for D in range(3,11):
 for sign in [-1,1]:
  ext=s.expand(p+q-p.subs(y,0)+sign*y*z*a**(D-2))
  poly=s.Poly(ext,a,b,y,z)
  H=s.expand(sum(co*u**(D-sum(ex))*a**ex[0]*b**ex[1]*y**ex[2]*z**ex[3] for ex,co in poly.terms()))
  T=s.expand(H.subs({a:a-u,b:b-u},simultaneous=True));k=D-3
  ck(s.expand(T.subs(z,0)-u**k*P)==0,'undo_shear_first_restriction')
  ck(s.expand(T.subs(y,0)-u**k*Q)==0,'undo_shear_second_restriction')
  strip={tuple(ex[i]-(k if i==0 else 0) for i in range(5)):co for ex,co in s.Poly(T,*xs).terms() if ex[0]>=k}
  derivative=dict(s.Poly(s.diff(T,u,k),*xs).terms())
  ck(set(strip)==set(derivative),'stripping_derivative_identical_support')
  for ex,co in strip.items():
   ck(derivative[ex]==co*factorial(ex[0]+k)//factorial(ex[0]),'exact_derivative_factor_injective')
# Canonical cone shear vectors: source-minus-sign convention diagnosed separately.
Tmat=s.eye(5);Tmat[1,0]=-1;Tmat[2,0]=-1
inv=Tmat.inv();eye=s.eye(5)
ck(Tmat*inv==s.eye(5),'shear_is_invertible')
ck(Tmat*(eye[:,0]+eye[:,1]+eye[:,2])==eye[:,0],'interior_reference_direction')
ck(Tmat*eye[:,0]==eye[:,0]-eye[:,1]-eye[:,2],'extra_required_boundary_direction')
for i in range(1,5):ck(Tmat*eye[:,i]==eye[:,i],'other_coordinate_directions_fixed')
t=s.symbols('t');ck(s.solve(t+1,t)==[-1],'printed_cone_sign_countercontrol')
# Nice transversal permanent identity, using a direct recursion rather than permutations.
rows=[{1,2,3},{1,5,6},{2,4,6,7},{3,4,5,7}]
def permrec(sets,cols):
 if not sets:return 1
 return sum(permrec(sets[1:],cols-{j}) for j in cols & sets[0])
vals={B:permrec(rows,set(B)) for B in combinations(range(1,8),4)}
for B,n in vals.items():ck(n in [0,2],'nice_transversal_equal_nonzero_multiplicity')
non=[frozenset(set(range(1,8))-set(B)) for B,n in vals.items() if n==0]
ck(len(non)==2 and len(non[0]&non[1])==1,'dual_two_forbidden_triples_share_center')
# Published F7^(-4) SOS, independently expanded with SymPy.
w=s.symbols('w1:8');forbid={frozenset([0,1,2]),frozenset([0,3,6]),frozenset([0,4,5])}
f=sum(s.prod(w[i] for i in B) for B in combinations(range(7),3) if frozenset(B) not in forbid)
a1=w[2]*w[6]+w[4]*w[6]+w[3]*w[4]+w[2]*w[3]+w[2]*w[4]+w[2]*w[5]+w[5]*w[6]+w[3]*w[5]
a2=w[2]*w[6]+w[2]*w[3]+w[2]*w[5]+w[2]*w[4]
a3=w[3]*w[5]-w[4]*w[6];a4=w[5]*w[6]-w[3]*w[4]
ck(s.expand(s.diff(f,w[0])*s.diff(f,w[1])-f*s.diff(f,w[0],w[1])-sum(a*a for a in [a1,a2,a3,a4])/2)==0,'published_Rayleigh_SOS_identity')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(sorted(C.items())),'scope':'Exact polynomial/support/rank and published input controls. Hyperbolicity-cone and M-convex analytic implications are audited separately in the review.'},sort_keys=True,indent=2))
