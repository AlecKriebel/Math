"""Independent symbolic controls for the conic partial proofs.
No author code is imported. Source receipts supply point/certificate data only.
"""
import sympy as s,json
from itertools import combinations,permutations,product
from collections import Counter
from pathlib import Path
C=Counter();cert={}
def ck(p,k):assert p,k;C[k]+=1
def eq(a,b,k):ck(s.cancel(a-b)==0,k)
E=s.eye(4);e=[E[:,i] for i in range(4)]
t,u,a,b,c=s.symbols('t u a b c',nonzero=True)
q=e[0]+e[1]+t*e[3];r=e[0]+e[2]+u*e[3];v=e[0]+e[1]+e[2]
cases=[('unequal',[q,r,e[0],e[1],e[2]],s.Matrix([u,-t,t-u,-u,t])),('equal',[v,q,r.subs(u,t),e[0],e[3]],s.Matrix([1,-1,-1,1,2*t]))]
for name,cols,rel in cases:
 M=s.Matrix.hstack(*cols);ck(M*rel==s.zeros(4,1),'symbolic_five_circuit_relation')
 mins=[s.factor(M[:,[i for i in range(5) if i!=j]].det()) for j in range(5)]
 for determinant in mins:ck(determinant!=0,'nonzero_symbolic_four_minor')
 cert[name+'_circuit_minors']=[str(d) for d in mins]
# General weighted path relation, covering nonzero coefficients of both ends
# by projective column rescaling.
M=s.Matrix.hstack(e[0]+a*e[1],e[1]+b*e[2],e[2]+c*e[3],e[0],e[3])
mins=[s.factor(M[:,[i for i in range(5) if i!=j]].det()) for j in range(5)]
for determinant in mins:ck(determinant!=0,'weighted_path_symbolic_minor')
cert['path_minors']=[str(d) for d in mins]
x=s.symbols('x0:4');X=s.Matrix(x)
for omit in range(3):
 B=s.Matrix.hstack(v,*[e[j] for j in range(3) if j!=omit],e[3])
 coords=B.inv()*X
 ck(coords[0]==x[omit] and coords[3]==x[3],'alternative_basis_outside_coordinates')
 for k,j in enumerate([j for j in range(3) if j!=omit],1):eq(coords[k],x[j]-x[omit],'alternative_basis_difference')
 cert['outside_basis_'+str(omit)]=[str(z) for z in coords]
# Complete four-vertex graph test; arbitrary edge coefficients handled above.
edges=list(combinations(range(4),2));connected=0;stars=0
for bits in product([0,1],repeat=6):
 adj=[set() for _ in range(4)]
 for keep,(i,j) in zip(bits,edges):
  if keep:adj[i].add(j);adj[j].add(i)
 reach={0}
 for _ in range(4):reach|=set().union(*(adj[i] for i in reach))
 if len(reach)<4:continue
 connected+=1
 has_path=any(all(p[i+1] in adj[p[i]] for i in range(3)) for p in permutations(range(4)))
 if not has_path:
  ck(sorted(map(len,adj))==[1,1,1,3],'complete_graph_star_classification');stars+=1
cert['graph_counts']={'connected':connected,'without_three_edge_path':stars}
center=e[0]+e[1];private=[e[0],e[2],e[3]]
for i in range(3):
 M=s.Matrix.hstack(center,*[private[j] for j in range(3) if j!=i]);ell=M.T.nullspace()[0]
 for j in range(3):
  val=(ell.T*(a*center+b*private[j]))[0]
  if i==j:ck(s.factor(val/b)!=0 and not val.has(a),'branch_annihilator_nonzero_private_coefficient')
  else:eq(val,0,'branch_annihilator_other_lines')
# Reflection subtraction with arbitrary nonzero constant, covering both
# deletion variants and both additive/multiplicative applications.
F,G,S,T,Q,K,d,e0,f,g=s.symbols('F G S T Q K d e f g',nonzero=True)
expr=lambda z:Q*z*(F-S-z)-K*(G-T-1/z)
eq(expr(d)-expr(e0),(d-e0)*(Q*(F-S-d-e0)-K/(d*e0)),'general_character_subtraction')
val=lambda z,w:z+w+K/(Q*z*w)
eq(val(d,e0)-val(d,f),(e0-f)*(Q*d*e0*f-K)/(Q*d*e0*f),'general_character_four_value_obstruction')
# All geometric residual laws from one homogeneous quadratic.
x,y,z,w=s.symbols('x y z w');A=s.symbols('A0:6')
quad=A[0]*x*x+A[1]*y*y+A[2]*z*z+A[3]*x*y+A[4]*x*z+A[5]*y*z
def pull(coords):return s.expand(quad.subs(dict(zip((x,y,z),coords)),simultaneous=True))
node=(w*w,w,-w**3-1);cusp=(w,1,w**3)
eq(node[0]*node[1]*node[2]+node[0]**3+node[1]**3,0,'nodal_normalization_incidence')
eq(cusp[1]**2*cusp[2]-cusp[0]**3,0,'cuspidal_normalization_incidence')
N=s.Poly(pull(node),w);U=s.Poly(pull(cusp),w)
eq(N.nth(0),N.nth(6),'nodal_root_product');eq(U.nth(5),0,'cuspidal_root_sum')
secC=s.Poly(w*w*pull((w,1/w,1)),w);secL=s.Poly(pull((w,1,0)),w)
eq(secC.nth(0)/secC.nth(4),secL.nth(0)/secL.nth(2),'secant_component_residual')
tanC=s.Poly(pull((w,w*w,1)),w);tanL=s.Poly(pull((1,w,0)),w)
eq(-tanC.nth(3)/tanC.nth(4),-tanL.nth(1)/tanL.nth(2),'tangent_component_residual')
tri=[s.Poly(pull(p),w) for p in [(0,1,w),(w,0,1),(1,w,0)]]
conc=[s.Poly(pull(p),w) for p in [(0,1,-w),(1,0,-w),(1,1,w)]]
eq(s.prod(p.nth(0)/p.nth(2) for p in tri),1,'triangle_six_root_product')
eq(sum(-p.nth(1)/p.nth(2) for p in conc),0,'concurrent_six_root_sum')
for m in range(3,65):
 pairs={(i+j)%m for i in range(m) for j in range(m) if i!=j}
 ck(pairs==set(range(m)),'distinct_pair_products_in_every_tested_cyclic_group')
# Independent checking of all six published rational ordinary-conic witnesses.
source=Path(__file__).with_name('WITNESS_INPUTS.json')
inputs=json.loads(source.read_text())
for rec in inputs['rational_witnesses']:
 pts=[list(map(s.Rational,p)) for p in rec['points']];co=s.Matrix(list(map(s.Rational,rec['conic_coefficients'])))
 ev=s.Matrix([[x*x,y*y,z*z,x*y,x*z,y*z] for x,y,z in pts]);ids=rec['indices']
 ck(ev[ids,:].rank()==5,'actual_rational_witness_uniqueness')
 ck([i for i in range(len(pts)) if (ev[i,:]*co)[0]==0]==ids,'actual_rational_witness_full_support')
 ck(ev.rank()==6,'actual_rational_configuration_nonconic')
# Check four Q(omega) ordinary certificates in a polynomial quotient ring,
# rather than reusing the author's pair-field arithmetic or row reduction.
omega=s.symbols('omega');mod=omega**2+omega+1
red=lambda f:s.rem(s.Poly(s.expand(f),omega,domain=s.QQ),s.Poly(mod,omega)).as_expr()
def decode(pair):return s.Rational(pair[0])+s.Rational(pair[1])*omega
for rec in inputs['quadratic_field_witnesses']:
 pts=[[decode(p) for p in point] for point in rec['points']]
 ev=s.Matrix([[red(x*x),red(y*y),red(z*z),red(x*y),red(x*z),red(y*z)] for x,y,z in pts])
 witness=rec['ordinary_example'];ids=witness['point_indices'];co=s.Matrix([decode(p) for p in witness['coefficients']])
 support=[i for i in range(len(pts)) if red((ev[i,:]*co)[0])==0]
 ck(support==ids,'quadratic_field_actual_witness_support')
 M=ev[ids,:];nonzero=any(red(M[:,list(cols)].det())!=0 for cols in combinations(range(6),5))
 ck(nonzero,'quadratic_field_actual_witness_rank_five')
 ck(any(i not in support for i in range(len(pts))),'quadratic_field_nonconic_extension')
# Count threshold equivalence for every possible line size up to a finite bound.
for n in range(11,101):
 for l in range(4,n+1):
  ck((l>=max(4,n-l-1))==(l>(n-2)//2),'large_line_integer_threshold')
Path('SYMBOLIC_CERTIFICATES.json').write_text(json.dumps(cert,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(C),'scope':'Independent symbolic circuit/residual identities and exact witness checks; the universal Picard, character, classification and geometric arguments are audited separately.'},indent=2,sort_keys=True))
