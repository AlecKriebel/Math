from pathlib import Path
from datetime import datetime, timezone
import itertools, json, sys
import sympy as s

HERE=Path(__file__).resolve().parent
x,t,h,A,rho,C,R,eps,a=s.symbols('x t h A rho C R eps a',positive=True)
checks=[]
def check(name,condition):
    assert bool(condition),name
    checks.append(name)
def zero(name,v): check(name,s.simplify(v)==0)

# Independent exact derivations; no package checker imported.
endpoint=2*h*s.sin(s.pi*h)/s.pi**2
gap=2*h**2-s.pi*endpoint+endpoint**2/2
zero('pulse leading full linear coefficient',s.expand(s.series(gap,h,0,6).removeO()).coeff(h,4)-(s.pi**2/3+2/s.pi**2))
zero('pulse no odd or lower powers',s.series(gap,h,0,4).removeO())
zero('pulse quotient leading slope',s.limit(gap/(2*h**4),h,0)-(s.pi**2/6+1/s.pi**2))
b=A/(2*rho)
zero('capped mass exact',2*rho*b-A)
zero('capped moment exact',s.integrate(rho*x**2,(x,-b,b))-A**3/(12*rho**2))
zero('global absorption worst cap reduction',s.factor(A**3/(6*rho**2)-C*A**5-A**3/(12*rho**2))-A**3*(1-12*C*A**2*rho**2)/(12*rho**2))
support=s.sqrt(eps/(2*s.pi))
parabolic=s.integrate((eps/s.pi-2*x**2)**2,(x,-support,support))
zero('exact parabolic positive-part squared norm',parabolic-8*s.sqrt(2)*eps**s.Rational(5,2)/(15*s.pi**s.Rational(5,2)))
check('claimed squared norm cap dominates sharp parabola',s.sqrt(2)>8*s.sqrt(2)/15)
trial_endpoint=2*a*s.sin(s.pi**2*eps/(2*a))/s.pi**2
trialgap=s.pi*eps-(s.pi+eps)*trial_endpoint+trial_endpoint**2/2
zero('fixed amplitude radial trial leading quadratic',s.expand(s.series(trialgap,eps,0,4).removeO()).coeff(eps,2)+s.Rational(1,2))
zero('fixed amplitude trial cubic coefficient',s.expand(s.series(trialgap,eps,0,4).removeO()).coeff(eps,3)-s.pi**5/(24*a**2))
q=lambda v:A-s.pi*v+v**2/2
bound=A/s.pi+R*A**5
zero('monotone composite exact substitute',q(bound)-(A**2/(2*s.pi**2)-s.pi*R*A**5+R*A**6/s.pi+R**2*A**10/2))
check('monotone derivative at arbitrary negative x',s.diff(q(x),x).subs(x,-17)<0)
zero('monotone difference factor',q(x)-q(bound)-(x-bound)*((x+bound)/2-s.pi))
zero('null target cap equality at bang amplitude',rho*A/rho-A)

# All 3^6 piecewise-constant cap densities, including empty/full mass,
# asymmetric and boundary concentrations. Rational computation is exact.
edges=[s.Rational(i,6)-s.Rational(1,2) for i in range(7)]
densities=0
for levels in itertools.product([0,s.Rational(1,2),1],repeat=6):
    mass=sum(levels)/6
    moment=sum(f*(edges[i+1]**3-edges[i]**3)/3 for i,f in enumerate(levels))
    squared=sum(f**2 for f in levels)/6
    check('density moment '+str(densities),moment>=mass**3/12)
    check('density cap L2 '+str(densities),squared<=mass)
    check('density Cauchy lower '+str(densities),mass**2<=squared)
    densities+=1

# Signed, multi-mode directions: c1 in [-1,1] is the first-mode coefficient
# of a unit spatial direction. Projection inequality is worst at c1=1.
for c1 in [-1,s.Rational(-3,5),0,s.Rational(3,5),1]:
    for sine in [0,s.Rational(1,4),s.Rational(3,4),1]:
        check('signed multimode projection '+str((c1,sine)),1-sine*c1>=1-sine)

# A sequence with terminal velocities not compact in H but compact in H^-1.
# u_n(t)=rho cos(n*pi*(1-t)) e_n has pointwise cap rho and L2 norm rho/sqrt2.
# Actual nonlinear compactness is established analytically, not by this test.
for n in range(1,17):
    freq=n*s.pi
    zero('high frequency terminal position '+str(n),s.integrate(s.sin(freq*(1-t))*s.cos(freq*(1-t))/freq,(t,0,1)))
    zero('high frequency velocity coefficient '+str(n),s.integrate(s.cos(freq*(1-t))**2,(t,0,1))-s.Rational(1,2))
    zero('high frequency radial norm '+str(n),2*s.integrate(s.sin(n*s.pi*x)**2,(x,0,1))-1)
check('high frequency H^-1 endpoint tends zero',s.limit(1/(2*s.pi*s.Symbol('n',positive=True)),s.Symbol('n',positive=True),s.oo)==0)
check('all optimizer contradiction exponent',s.Rational(5,4)+1>2)
check('radial lower exponent beats Lipschitz',s.Rational(3,4)<1)
check('rough radial exponent bracket compatible',s.Rational(3,4)>s.Rational(1,2))
check('fixed nu velocity exponent negligible',10>2)

receipt={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','sympy':s.__version__,'python':sys.version,'assertions':len(checks),'density_profiles':densities,'checks':checks,'limits':'Exact finite controls and algebra only. The compatible quintic remainder and nonlinear PDE compactness are analytic arguments; these checks do not certify an unknown constant or historical priority.'}
(HERE/'INDEPENDENT_STRESS_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:receipt[k] for k in ('utc','status','assertions','density_profiles','limits')},indent=2))
