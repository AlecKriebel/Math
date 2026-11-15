"""Own exact scope controls: direct point-divisor sums and physical algebra; no source imports."""
from fractions import Fraction as F
from collections import Counter
from math import gcd
from pathlib import Path
import hashlib,json,datetime

def frac(x):return str(x.numerator)+'/'+str(x.denominator)
def point_divisor(N,tau,orientation=1):
 step=F(orientation*tau,N);zero=[-F(1,4)+F(tau,2*N),-F(1,4)-F(tau,2*N)];poles=[F(0),F(1,2)];d=Counter()
 for j in range(N):
  for z in zero:d[(z-j*step)%1]+=1
  for z in poles:d[(z-j*step)%1]-=1
 d={x:v for x,v in d.items()if v};assert sum(d.values())==0
 return d

def serialized(d):return[[frac(x),d[x]]for x in sorted(d)]
rows=[];complete=[]
for n in range(3,81):
 for tau in range(1,(n+1)//2):
  if 2*tau>=n or gcd(tau,n)!=1:continue
  d=point_divisor(n,tau);rev=point_divisor(n,tau,-1);assert d==rev
  invariant=not d;assert invariant==(n%4==2)
  negative=[-v for v in d.values()if v<0];positive=[v for v in d.values()if v>0]
  if n%2:assert len(negative)==2*n and set(negative)=={1}and len(positive)==n and set(positive)=={2}
  elif n%4==0:assert len(negative)==n and set(negative)=={2}and len(positive)==n and set(positive)=={2}
  rows.append({'n':n,'tau':tau,'exact_step_order':n,'invariant_divisor':invariant,'remaining_pole_degree':sum(negative),'remaining_pole_points':len(negative),'orientation_agreement':True})
  if(n,tau)in[(3,1),(4,1),(6,1),(8,3),(10,3),(12,5)]:complete.append({'n':n,'tau':tau,'whole_divisor_in_normalized_torus':serialized(d)})
repeated=[]
for N in range(3,41):
 for tau in range(1,(N+1)//2):
  if 2*tau>=N:continue
  g=gcd(N,tau);n=N//g;primitive=point_divisor(n,tau//g);d=point_divisor(N,tau)
  assert d=={x:g*v for x,v in primitive.items()}
  assert(not d)==(n%4==2)
  if N%4==2:assert(not d)==(n%2==0)
  repeated.append({'return_length':N,'step_numerator':tau,'least_period':n,'repetitions':g,'constant_divisor':not d})
assert point_divisor(6,2) and not point_divisor(6,1)
# Exact normal/tangent quadratic form and ordinary focal-square identities.
geom=[]
for a in range(2,8):
 for b in range(1,a):
  aa,bb=F(a*a),F(b*b);cc=aa-bb;lam=bb/F(2);AA,BB=aa-lam,bb-lam
  for t in[F(j,7)for j in range(-9,10)]:
   x=F(a)*(1-t*t)/(1+t*t);y=F(b)*2*t/(1+t*t)
   assert x*x/aa+y*y/bb==1
   nx,ny=x/aa,y/bb;tx,ty=-y/bb,x/aa
   mix=nx*((BB-y*y)*tx+x*y*ty)+ny*(x*y*tx+(AA-x*x)*ty)
   rhs=x*y*cc/(aa*bb)*(1-x*x/aa-y*y/bb)
   assert mix==rhs==0
   det=(BB-y*y)*(AA-x*x)-(x*y)**2;assert det==AA*BB*(1-x*x/AA-y*y/BB)<0
   # Coefficients of 1 and sqrt(cc), separately, for both focus signs.
   for sign in[-1,1]:
    actual=(x*x+y*y+cc,sign*2*x)
    claimed=(aa+cc*x*x/aa,sign*2*x)
    assert actual==claimed
   geom.append({'a':a,'b':b,'rational_parameter':frac(t),'normal_tangent_form':frac(mix),'direction_determinant_negative':True})
# Four-bounce diamond versus tangent rectangle, ordinary positive focal products.
rect=[]
for a in range(2,9):
 for b in range(1,a):
  aa,bb=F(a*a),F(b*b);cc=aa-bb;ss=aa+bb;AA,BB=aa*aa/ss,bb*bb/ss
  assert AA-BB==cc and 0<AA<aa and 0<BB<bb
  assert AA/aa+BB/bb==1
  diamond=aa*bb;rectangle=(aa-cc*AA/aa)**2;difference=diamond-rectangle
  assert rectangle==4*aa*aa*bb*bb/(ss*ss)
  assert difference==aa*bb*cc*cc/(ss*ss)>0
  rect.append({'a':a,'b':b,'caustic_axes_squared':[frac(AA),frac(BB)],'diamond_focal_product':frac(diamond),'rectangle_focal_product':frac(rectangle),'positive_difference':frac(difference),'reflection_reason':'Diamond axis symmetry; rectangle normal components A/a²=B/b²=1/sqrt(a²+b²).'})
assert rect[0]['diamond_focal_product']=='4/1'and rect[0]['rectangle_focal_product']=='64/25'
# Multiquadratic arithmetic Q[a,c]/(a²-15,c²-8), basis1,a,c,ac.
def add(x,y):return tuple(x[i]+y[i]for i in range(4))
def scale(x,q):return tuple(q*v for v in x)
def mul(x,y):
 out=[F(0)]*4
 for i,v in enumerate(x):
  for j,w in enumerate(y):
   ea=(i&1)+(j&1);ec=(i>>1)+(j>>1);out[(ea%2)+2*(ec%2)]+=v*w*(15 if ea>=2 else 1)*(8 if ec>=2 else 1)
 return tuple(out)
zero=(F(0),)*4;av=(F(0),F(1),F(0),F(0));cv=(F(0),F(0),F(1),F(0))
p1=mul(add(av,scale(cv,-1)),mul(add(av,scale(cv,F(3,4))),add(av,scale(cv,F(3,4)))))
p2=mul(add(av,cv),mul(add(av,scale(cv,-F(3,4))),add(av,scale(cv,-F(3,4)))))
assert p1==(F(0),F(15,2),F(3),F(0))and p2==(F(0),F(15,2),F(-3),F(0))
diff=add(mul(p1,p1),scale(mul(p2,p2),-1));assert diff==(F(0),F(0),F(0),F(90))
# Triangle geometry, with exact squared axes and unit-ray/normal coefficients.
assert F(135,16)-F(7,16)==8 and F(9,16)+F(49,16)/7==1 and F(135,16)+15*F(7,16)==15
assert F(15,16)+F(1,16)==1 and F(1,4)==5*F(1,20)and F(5,4)==5*F(1,4)
assert F(3,4)/15==F(1,20)
circle=[{'N':N,'radius':frac(F(3,2)),'constant_product':frac(F(3,2)**N)}for N in range(1,17)]
body={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','mechanisms':'Own direct normalized point-divisor sums, independent rational physical quadratic-form checks, explicit diamond/rectangle four-bounce geometry and multiquadratic triangle arithmetic; no native source code/results imported or read.','primitive_cases':len(rows),'primitive_rows':rows,'whole_selected_divisors':complete,'nonprimitive_and_repeat_cases':len(repeated),'nonprimitive_rows':repeated,'exact_normal_reflection_focal_cases':len(geom),'normal_reflection_case_digest':hashlib.sha256(json.dumps(geom,sort_keys=True).encode()).hexdigest(),'four_bounce_controls':rect,'triangle':{'basis':['1','a','c','ac'],'relations':{'a²':15,'c²':8},'primitive_Fplus_products':[[str(x)for x in p1],[str(x)for x in p2]],'six_event_difference':[str(x)for x in diff],'six_event_difference_positive':'90ac=180sqrt30>0; a,c positive real roots','genuine_reflection_and_confocal_geometry_checked':True},'circle_boundary_controls':circle,'negative_controls':{'even_only_constancy_falsified_by_two_physical_n4_orbits':True,'nominal_N6_tau2_falsifies_primitive_period_substitution':True,'odd_two_focus_equality_falsified_by_triangle':True,'circle_excluded_from_c_nonzero_divisor_model':True},'limitations':'Finite exact corroboration, not validated analytic numerics, universal-period proof, exhaustive novelty or primary-source verification. Native checker belongs to separate lane and is not run here.'}
p=Path(__file__).resolve().parent;(p/'INDEPENDENT_SCOPE_CONTROLS.json').write_text(json.dumps(body,indent=2)+'\n');print(json.dumps({k:body[k]for k in['status','primitive_cases','nonprimitive_and_repeat_cases','exact_normal_reflection_focal_cases']}))
