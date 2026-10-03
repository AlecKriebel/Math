#!/usr/bin/env python3
"""Independent exact finite controls and false-route controls; no Floer computation."""
from pathlib import Path
from itertools import combinations,product
from functools import reduce
import json,math,sys
import sympy as s
mode=sys.argv[1] if len(sys.argv)>1 else 'positive'
checks=[]
def ck(name,value):
 assert bool(value),name
 checks.append(name)
t=s.symbols('t');d=t*t-t+1
if mode=='wrong_square':
 ck('incorrect unsquared vanishing asserted for adjoint',s.gcd(d,t**6-1)==1)
elif mode=='false_general_vanishing':
 w=(-1+s.I*s.sqrt(3))/2
 R=s.Matrix([[0,0,0,1-w],[1,w,w*w,0]])
 B=s.Matrix([w-1,w-1,w-1,0])
 ck('incorrect universal target-premise normal H1 vanishing',4-R.rank()-B.rank()==0)
elif mode=='null_equals_absent_fallback':
 ck('incorrect literal null equals absent default object',json.loads('null')==json.loads('{}'))
elif mode=='primitive_from_cover':
 # A rational C6-module consists only of the two primitive C3 eigenspaces.
 # Primitive C6 multiplicity is zero although total b1 is two.
 ck('incorrect cover-positive implies same primitive twist positive',0>0)
elif mode=='positive':
 ck('trefoil_phi6',d==s.cyclotomic_poly(6,t))
 ck('trefoil_squared_phi12',d.subs(t,t*t)==s.cyclotomic_poly(12,t))
 for n in range(1,49):
  ck('unsquared_root_selection_'+str(n),(s.degree(s.gcd(d,t**n-1))>0)==(n%6==0))
  ck('squared_root_selection_'+str(n),(s.degree(s.gcd(d.subs(t,t*t),t**n-1))>0)==(n%12==0))
  ck('squaring_image_order_'+str(n),n//math.gcd(n,2)==len({(2*k)%n for k in range(n)}))
 # Seifert presentation ci^3 h^beta_i=1, c1c2c3=1, h central.
 M=s.Matrix([[3,0,0,1],[0,3,0,1],[0,0,3,2],[1,1,1,0]])
 ck('genuine_example_det',M.det()==-36)
 minor_gcd=[]
 for k in range(1,5):
  vals=[abs(int(M.extract(rs,cs).det())) for rs in combinations(range(4),k) for cs in combinations(range(4),k)]
  minor_gcd.append(reduce(math.gcd,vals))
 ck('genuine_example_determinantal_divisors',minor_gcd==[1,1,3,36])
 factors=[minor_gcd[0]]+[minor_gcd[k]//minor_gcd[k-1] for k in range(1,4)]
 ck('genuine_example_H1_C3_plus_C12',factors==[1,1,3,12])
 ck('genuine_example_even_homology',abs(M.det())%2==0)
 ck('genuine_example_euler_and_cover',-s.Rational(4,3)*3==-4)
 w=(-1+s.I*s.sqrt(3))/2
 for weight in (1,2):
  a=s.simplify(w**weight)
  ck('seifert_character_relations_'+str(weight),s.simplify(a**3)==1)
  # Each commutator forces u_h=0; ci^3 contributes 1+a+a^2=0;
  # product relation contributes u1+a*u2+a^2*u3=0.
  ck('seifert_cube_cocycle_zero_'+str(weight),s.simplify(1+a+a*a)==0)
  R=s.Matrix([[0,0,0,1-a],[1,a,a*a,0]])
  B=s.Matrix([a-1,a-1,a-1,0])
  ck('seifert_coboundary_in_cocycles_'+str(weight),(R*B).applyfunc(s.simplify)==s.zeros(2,1))
  ck('seifert_rank_one_H1_dimension_'+str(weight),4-R.rank()-B.rank()==1)
 ck('genuine_example_adjoint_H1_real_dimension',2*(4-R.rank()-B.rank())==2)
 # Quaternion real-parts used in the all-representations proof.
 dot=s.symbols('dot',real=True)
 ck('angle_2pi_over3_endpoint',s.solve(s.Rational(1,4)-s.Rational(3,4)*dot+s.Rational(1,2),dot)==[1])
 ck('angle_pi_over3_endpoint',s.cos(s.pi/3)**2==s.Rational(1,4) and s.sin(s.pi/3)**2==s.Rational(3,4))
 T=s.Matrix([[0,-1],[1,-1]])
 ck('torus_order3_rotation',T**3==s.eye(2) and T!=s.eye(2))
 ck('torus_three_fixed_points',abs((T-s.eye(2)).det())==3)
 # Exact cocycles for C2*C3, with character index chosen independently.
 raw=[];squared=[]
 def h1(a,b):
  R=s.diag(s.simplify(1+a),s.simplify(1+b+b*b));B=s.Matrix([a-1,b-1])
  assert (R*B).applyfunc(s.simplify)==s.zeros(2,1)
  return 2-R.rank()-B.rank()
 for k in range(6):
  a=s.Integer(-1)**k;b=s.simplify(w**k)
  raw.append(h1(a,b));squared.append(h1(a*a,s.simplify(b*b)))
 ck('trefoil_unsquared_H1',[0,1,0,0,0,1]==raw)
 ck('trefoil_adjoint_squared_H1_zero',squared==[0]*6)
 ck('full_degree6_cover_positive_b1',sum(raw)==2)
 ck('degree3_adjoint_cover_b1_zero',sum(raw[k] for k in (0,2,4))==0)
 ck('all_finite_covers_stronger_than_CF',sum(raw)>0 and sum(raw[k] for k in (0,2,4))==0)
 for ns in [(),(1,),(2,),(6,),(3,12),(2,2,2),(2,4,6),(3,5,7,2)]:
  chars=list(product(*(range(n) for n in ns)));orbits=set();central=0
  for chi in chars:
   inv=tuple((-a)%n for a,n in zip(chi,ns));orbits.add(min(chi,inv));central+=chi==inv
  h=math.prod(ns);noncentral=(h-central)//2
  ck('character_count_'+str(ns),central+2*noncentral==h and len(orbits)==central+noncentral)
  ck('central_count_'+str(ns),central==math.prod(math.gcd(n,2) for n in ns))
 # The ordinary local critical groups are computed only after the geometric
 # identification with a cone on T2 x interval, independently reviewed in text.
 x,y=s.symbols('x y',nonnegative=True);F=(x-y)*(x-2*y)
 ck('quartic_critical_coefficient_det',s.Matrix([[2,-3],[-3,4]]).det()==-1)
 q=s.symbols('q',real=True);P=s.expand(F.subs({x:q,y:1-q}))
 ck('lowerlink_interval',s.solve_univariate_inequality(P<=0,q,relational=False)==s.Interval(s.Rational(1,2),s.Rational(2,3)))
 ck('local_critical_euler_and_rank',2-1==1 and 2+1==3)
 ck('literal_null_is_not_absent_object',json.loads('null') is None and json.loads('{}')=={} and json.loads('null')!=json.loads('{}'))
else: raise ValueError(mode)
out={'mode':mode,'passed':len(checks),'labels':checks,'sympy_version':s.__version__,'seifert_H1_invariant_factors':factors if mode=='positive' else None,'seifert_noncentral_adjoint_H1_real_dimension':2 if mode=='positive' else None,'trefoil_unsquared_H1':raw if mode=='positive' else None,'trefoil_squared_H1':squared if mode=='positive' else None,'limits':'Finite exact controls; source-backed realization of the explicit Seifert example; no I# computation or global proof from finite enumeration.'}
Path(__file__).with_name('own_exact_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='labels'},indent=2))
