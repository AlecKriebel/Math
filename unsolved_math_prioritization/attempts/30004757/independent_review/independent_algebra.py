#!/usr/bin/env python3
"""Review-side exact calculations. No source PDE solver or asymptotic matching claim."""
import json
import sympy as S
checks=[]
def ck(name, value):
    v=S.factor(S.simplify(value))
    assert v == 0, (name, v)
    checks.append(name)
r,z,R,s,t,lam=S.symbols('r z R s t lam', positive=True)
x=S.symbols('x', real=True)
for n in (3,4):
    alpha=S.Rational(n,n-2)
    gamma=S.Rational(2*(n-1),n-2)
    # Direct differentiation of Mooney's unnormalized crease barrier.
    raw=(r**gamma+z*z/r**gamma)/2
    det=(S.diff(raw,r)/r)**(n-2)*(S.diff(raw,r,2)*S.diff(raw,z,2)-S.diff(raw,r,z)**2)
    norm=(gamma/2)**(n-1)*(gamma-1)
    ck(f'crease barrier determinant n={n}',det-norm*(1-z*z/r**(2*gamma))**(n-1))
    ck(f'crease barrier value matching n={n}',raw.subs(z,r**gamma)-r**gamma)
    ck(f'crease barrier radial derivative matching n={n}',S.diff(raw,r).subs(z,r**gamma))
    ck(f'crease barrier axial derivative matching n={n}',S.diff(raw,z).subs(z,r**gamma)-1)
    # Full n-dimensional Hessian under the parabolic variable, at arbitrary y.
    y=S.symbols('y0:'+str(n-2), real=True)
    ss=x+sum(yi*yi for yi in y)/(2*R)
    Phi=S.Function('Phi')
    V=Phi(s,z)
    expr=V.subs(s,ss)
    hess=S.hessian(expr,(x,*y,z))
    determinant=S.factor(hess.det(method='domain-ge'))
    expected=((S.diff(V,s)/R)**(n-2)*(S.diff(V,s,2)*S.diff(V,z,2)-S.diff(V,s,z)**2)).subs(s,ss)
    ck(f'full parabolic-coordinate Hessian n={n}',determinant-expected)
    # Scaling checked as a full coordinate-Jacobian transformation.
    jac_exponent=1+S.Rational(n-2,2)+alpha
    ck(f'full scaling determinant n={n}',2*jac_exponent-n*alpha)
    eta=S.symbols('eta', real=True)
    B=S.symbols('B',positive=True)
    b0,c0=S.symbols('b0 c0',positive=True)
    b=(b0**n-n*c0*eta**2/2)**S.Rational(1,n)
    ck(f'profile first integral n={n}',S.diff(b,eta)+c0*eta/b**(n-1))
    # Indicial equation independently from logarithmic derivative q=x*b'/b.
    k=S.symbols('k')
    # Linearized normalized equation at b=C*x^alpha.
    e=S.symbols('e')
    f=t**alpha*(1+e*t**k)
    res=S.diff(f,t)**(n-2)*S.diff(f,t,2)-alpha**(n-1)*(alpha-1)*f
    poly=S.simplify(S.diff(res,e).subs(e,0)/t**(alpha+k)/alpha**(n-2))
    ck(f'ODE stable exponents n={n}',poly-(k+1)*(k+(6 if n==3 else 4)))
    # Radial exterior and dual derivative functions independently invert each other.
    p=(r**n-R**n)**S.Rational(1,n)
    ck(f'radial exterior density n={n}',S.diff(p,r)*(p/r)**(n-1)-1)
    q=(r**n+R**n)**S.Rational(1,n)
    ck(f'radial dual density n={n}',S.diff(q,r)*(q/r)**(n-1)-1)
    # General unimodular diagonal angular calibration, not a unit principal axis.
    d=S.symbols('d0:'+str(n),positive=True)
    dlast=1/S.prod(d[:-1]); vals=list(d[:-1])+[dlast]
    radialcoef=R**(1-n)*vals[0]**(n+1)/(n*(n+1))
    tangentdet=R**(n-1)*S.prod(v*v for v in vals[1:])/vals[0]**(n-1)
    ck(f'unimodular ellipsoid coefficient n={n}',n*(n+1)*radialcoef*tangentdet-1)
    # Fixed-weight isotropic scaling: atom Jacobian s^n, quadratic term unchanged.
    c=S.symbols('c'); Q=r*r/2-c
    ck(f'fixed normalization rescaling n={n}',s*s*Q.subs(r,r/s)+(s*s-1)*c-Q)
# The half-ball support limit has unequal second normal derivatives.
upper=R*S.sqrt(1+t*t)
ck('upper half-ball second derivative',S.diff(upper,t,2).subs(t,0)-R)
ck('lower half-ball second derivative',S.diff(R,t,2))
print(json.dumps({'status':'PASS','checks':len(checks),'verified':checks,
  'sympy_version':S.__version__,
  'scope':'Exact symbolic checks only. The analytic review supplies the convexity, comparison, compactness and source hypotheses; neither artifact solves the original fixed-separation problem.'},indent=2))
