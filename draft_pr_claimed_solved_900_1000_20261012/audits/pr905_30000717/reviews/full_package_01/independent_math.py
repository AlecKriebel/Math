from pathlib import Path
import sympy as s,json,datetime
W=Path(__file__).resolve().parent
x,y,z,u=s.symbols('x y z u',real=True);vs=(x,y,z)
R=x**6+y**6+z**6-x**4*y**2-x**2*y**4-x**4*z**2-x**2*z**4-y**4*z**2-y**2*z**4+3*x**2*y**2*z**2
Z=[(1,a,b) for a in (1,-1) for b in (1,-1)]+[(1,a,0) for a in (1,-1)]+[(1,0,b) for b in (1,-1)]+[(0,1,b) for b in (1,-1)]
checks=[]
def req(c,m):
 if not c:raise RuntimeError(m)
 checks.append(m)
def restrict(p,v):return s.expand(p.subs(dict(zip(vs,[u*a for a in v])),simultaneous=True))
grad=[s.diff(R,v) for v in vs];J=[vs[j]*grad[i]-vs[i]*grad[j] for i,j in [(0,1),(0,2),(1,2)]];K=[g for i,j in [(0,1),(0,2),(1,2)] for g in [vs[j]*grad[i],vs[i]*grad[j]]]
a,b,c=s.symbols('a b c',nonnegative=True);F=a**3+b**3+c**3-a*a*b-a*b*b-a*a*c-a*c*c-b*b*c-b*c*c+3*a*b*c
req(s.expand(F-((a-b)**2*(a+b-c)+c*(a-c)*(b-c)))==0,'Schur identity');req(s.expand(F.subs({a:x*x,b:y*y,c:z*z})-R)==0,'specialization')
for v in Z:
 req(restrict(R,v)==0,'R zero whole line '+str(v));req(all(restrict(g,v)==0 for g in grad),'gradient zero whole line '+str(v))
for v in [(1,0,0),(0,1,0),(0,0,1)]:
 req(restrict(R,v)==u**6,'axis value '+str(v));req(all(restrict(g,v)==0 for g in J+K),'axis in both varieties '+str(v))
def mons(d):return [x**i*y**j*z**(d-i-j) for i in range(d+1) for j in range(d-i+1)]
def evalm(d,points=Z):return s.Matrix([[p.subs(dict(zip(vs,v))) for p in mons(d)] for v in points])
ranks={str(d):evalm(d).rank() for d in range(8)}
for d in range(4):req(evalm(d).rank()==len(mons(d)),'injective homogeneous evaluation degree '+str(d))
req(evalm(3).det()==-128,'cubic determinant in original order')
# NEW sensitivity check: every direction is necessary for this cubic injectivity.
deletion=[]
for i,v in enumerate(Z):
 M=evalm(3,Z[:i]+Z[i+1:]);req(M.rank()==9,'nine-directions rank '+str(v)); q=s.expand(sum(m*t for m,t in zip(mons(3),M.nullspace()[0])));req(q.subs(dict(zip(vs,v)))!=0,'omitted-point witness '+str(v));deletion.append({'removed':v,'witness':str(q)})
# NEW higher-degree escape attempt: find a quartic allowed by zero lines with a positive-axis restriction.
M=evalm(4); quartics=[s.expand(sum(m*t for m,t in zip(mons(4),n))) for n in M.nullspace()]
axis_q=next(q for q in quartics if restrict(q,(1,0,0))!=0)
req(all(restrict(axis_q,v)==0 for v in Z),'quartic vanishes on entire zero lines');req(s.degree(restrict(axis_q,(1,0,0)),u)==4,'quartic can survive on positive axis')
# This demonstrates why eliminating all positive homogeneous degrees would be false.
# Independent algebraic positive controls for the real/finite restrictions.
req(s.expand(u**8+(s.I*u**4)**2)==0,'complex leading-square cancellation exists outside claim')
req(s.expand(((u**6+1)/2)**2-((u**6-1)/2)**2)==u**6,'signed-square certificate exists outside claim')
# NEW positive certificate control: nonnegative sextic x^6 permits an ideal-only certificate.
for e in [s.Rational(0),s.Rational(1,10**30),s.Integer(10)**30,s.sqrt(2)]:
 req(s.simplify(x**6+e-(x**3)**2-s.sqrt(e)**2)==0,'x6 positive control epsilon '+str(e))
# NEW shift and scaling checks: any real constant preserves both derivative-defined ideals;
# positive scale does so up to invertible scalar, but negative scale fails nonnegativity on axes.
t=s.symbols('t',real=True);req(all(s.diff(R+t,v)==g for v,g in zip(vs,grad)),'arbitrary shift preserves derivatives');req(restrict(-R,(1,0,0))==-u**6,'negative scaling outside nonnegativity hypothesis')
req(s.expand(sum(v*g for v,g in zip(vs,grad))-6*R)==0,'Euler gradient-ideal compatibility')
# Literal product diagnostic and a NEW exact ideal-radical route, not just a branch proof.
Q=(1-x*y)**2+y*y-s.Rational(1,2);q1=s.expand(y*s.diff(Q,x));q2=s.expand(x*s.diff(Q,y));gb=s.groebner([q1,q2],x,y)
# Over R or C, products imply the origin; powers of both coordinates reduce to zero.
powers={}
for v in (x,y):
 power=next(n for n in range(1,8) if gb.reduce(v**n)[1]==0);powers[str(v)]=power;req(gb.reduce(v**power)[1]==0,'literal product coordinate-power ideal membership '+str(v))
req(s.simplify(Q.subs({x:1/u,y:u},simultaneous=True))==u*u-s.Rational(1,2),'nonattaining reciprocal path')
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_INDEPENDENT_MATHEMATICAL_CONTROLS','sympy_version':s.__version__,'guards':len(checks),'guards_detail':checks,'rank_degrees_0_to_7':ranks,'single_direction_deletion_cubic_witnesses':deletion,'quartic_axis_escape_witness':str(axis_q),'quartic_axis_restriction':str(restrict(axis_q,(1,0,0))),'literal_product_groebner_basis':[str(p.as_expr()) for p in gb.polys],'literal_product_coordinate_powers':powers,'scope':'Finite exact supporting checks and boundary falsification controls, supplementing reconstructed universal real finite-SOS proof.'}
print(json.dumps(result,indent=2))
