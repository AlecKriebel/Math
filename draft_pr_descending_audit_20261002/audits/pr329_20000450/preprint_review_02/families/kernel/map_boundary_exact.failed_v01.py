"""Exact inverse-chart poles, marked-point slopes, and plane-vertex collisions."""
import json, sympy as S
r=S.sqrt(5); lam,x,b,v=S.symbols('lambda x beta v')
phi=(1+r)/2;c=(11+5*r)/2;d=5+2*r
alpha=1-r/5;gamma=2*r/5;e=gamma-alpha
beta=(11-5*r)*lam/(2*(lam+5*r));k=4*(lam+5*r)/r;q=d*k*k
a=40+20*r+8*lam;B0=a+5
a3=(-112+48*r)*lam**2*(lam+5*r)/5
checks=[]
def norm(z): return S.cancel(z,extension=r)
def ck(n,z):
    z=norm(z)
    if z != 0: raise AssertionError(n+': '+str(z))
    checks.append(n)
z=a3/(q*(x-beta))-alpha*lam;t=z-d
ck('z+gamma*lambda pole identity',z+gamma*lam-e*lam*x/(x-beta))
ck('X denominator identity',a+4*r*t-4*r*(z+gamma*lam))
ck('z rational form',z-lam*(-alpha*x+gamma*beta)/(x-beta))
# On residual points xi=q(x-beta), eta=k^3*d*delta*v. All constants are
# nonzero over K for lambda not 0,-5r,-c. x=0,beta are excluded by R values.
X=norm((B0-t*t)/(a+4*r*t))
Y_over_delta=norm(k*v*(-alpha*x+gamma*beta)/(20*e*x*(x-beta)))
ratio_times_delta=norm(X/Y_over_delta)
# Ratio X/Y = ratio_times_delta/delta, interpreted at marked points by a local
# parameter; both v values specialize nonzero, hence both X,Y poles are simple.
at0_plus=norm(S.limit(ratio_times_delta.subs(v,beta/2),x,0))
atb_plus=norm(S.limit(ratio_times_delta.subs(v,beta**2/2),x,beta))
ck('x=0 positive-v infinity slope is r/delta',at0_plus-r)
ck('x=beta positive-v infinity slope is -delta',atb_plus+d)
ck('vertex abscissa is phi*beta',beta+a3/(q*alpha*lam)-phi*beta)
ck('z=0 maps to X=1',X.subs(x,phi*beta)-1)
ck('z=0 maps to Y=0 for both ordinates',Y_over_delta.subs(x,phi*beta))
T=4*x**3+(b*b-6*b+1)*x*x+2*(b*b-b)*x+b*b
R=5*x**10+5*(b*b-5*b+1)*x**9+(b**4-7*b**3+44*b*b-38*b+1)*x**8+b*(b**4+3*b**3-26*b*b+127*b-9)*x**7+b*b*(b**4+3*b**3+19*b*b-248*b+36)*x**6+b**3*(b**4+3*b**3-71*b*b+322*b-84)*x**5+b**4*(b**4-12*b**3+94*b*b-293*b+126)*x**4+5*b**5*(b**3-10*b*b+36*b-25)*x**3+5*b**6*(2*b*b-13*b+16)*x*x+10*b**7*(b-3)*x+5*b**8
vertexT=S.factor(T.subs(x,phi*b),extension=r)
vertexR=S.factor(R.subs(x,phi*b),extension=r)
vertexRlambda=S.factor(R.subs({x:phi*beta,b:beta}),extension=r)
vertexTlambda=S.factor(T.subs({x:phi*beta,b:beta}),extension=r)
print(json.dumps({'status':'EXACT_PASS','checks':checks,
 'marked_images':{'O':'[0:1:0]','(0,0)':'X/Y=-r/delta','(0,beta)':'X/Y=r/delta','(beta,0)':'X/Y=delta','(beta,beta^2)':'X/Y=-delta'},
 'X_rational_Tate':str(X),'Y_over_delta':str(Y_over_delta),
 'vertex_T_beta':str(vertexT),'vertex_R_beta':str(vertexR),
 'vertex_T_lambda':str(vertexTlambda),'vertex_R_lambda':str(vertexRlambda),
 'meaning':'At any nonsingular beta root of the displayed vertex R factor, the two distinct normalization fifth-torsion points at x=phi*beta both map to the plane vertex [1:0:1]. This does not duplicate normalization coordinates.'},indent=2))
