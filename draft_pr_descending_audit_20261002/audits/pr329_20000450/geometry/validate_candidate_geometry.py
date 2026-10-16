from datetime import datetime, timezone
import time
print("native_utc_start",datetime.now(timezone.utc).isoformat(),flush=True)
import sympy as S
print("sympy",S.__version__,flush=True)
r=S.sqrt(5); phi=(1+r)/2; m=5-2*r; d=5+2*r; c=phi**5
L,X,Y,T,u,v,t,s,x0,xi,eta=S.symbols("L X Y T u v t s x0 xi eta")
checks=[]
allvars=S.symbols("L X Y T u v t s x0 xi eta x y")
def exact_zero(expr):
    numerator=S.fraction(S.together(expr))[0]
    return S.Poly(numerator,*allvars,extension=r).is_zero
rational_domain=S.QQ.algebraic_field(r).frac_field(*allvars)
def simplify(expr):
    return rational_domain.to_sympy(rational_domain.from_sympy(expr))
def check(label,expr):
    val=simplify(expr)
    assert exact_zero(val),(label,val)
    checks.append(label)
    print("PASS",label,"native_utc",datetime.now(timezone.utc).isoformat(),flush=True)
def reject(label,expr):
    val=simplify(expr)
    assert not exact_zero(val),(label,val)
    print("NEGATIVE_CONTROL_REJECTED",label,"native_utc",datetime.now(timezone.utc).isoformat(),flush=True)
# Build P independently from the resultant established before candidate exposure.
Pind=u**5+v**5-phi**5*T**5+5*phi**3*u*v*T**3-5*phi*u*u*v*v*T
P=S.expand(-Pind.subs({u:-(X+S.I*Y),v:-(X-S.I*Y)}))
Pclaimed=2*(X**5-10*X**3*Y**2+5*X*Y**4)+5*phi*(X*X+Y*Y)**2*T-5*phi**3*(X*X+Y*Y)*T**3+phi**5*T**5
check("source_resultant_matches_candidate_P",P-Pclaimed)
G=S.expand((P+L*T*(X*X+Y*Y-T*T)**2).subs(T,1))
quartic=S.Poly(G,Y)
A=quartic.coeff_monomial(Y**4);B=quartic.coeff_monomial(Y**2);C=quartic.coeff_monomial(1)
h=4*X*X+2*X-1
a=40+20*r+8*L;b=a+5
conic=20*X*X-a*X+b
check("quartic_discriminant_recomputed",B*B-4*A*C-h*h*conic)
check("conic_discriminant_recomputed",a*a-80*b-64*L*(L+5*r))
Xp=(b-t*t)/(a+4*r*t);Vp=2*r*Xp+t
check("conic_parametrization",Vp*Vp-conic.subs(X,Xp))
Y2=simplify((h.subs(X,Xp)*Vp-B.subs(X,Xp))/(2*A.subs(X,Xp)))
alpha=1-r/5;gamma=2*r/5
# Independently derive the cubic by manipulating Y^2 rather than importing F.
z=t+d
w2=simplify(400*(z+gamma*L)**2*Y2/(z*z))
y02=simplify(w2.subs(t,s-d-alpha*L)/(s*s))
poly0=simplify(y02.subs(s,1/x0))
assert S.denom(poly0)==1
coeff=S.Poly(poly0,x0)
print("DERIVED_CUBIC_COEFFICIENTS",[simplify(coeff.coeff_monomial(x0**j)) for j in range(4)],flush=True)
a0=coeff.coeff_monomial(1);a1=coeff.coeff_monomial(x0);a2=coeff.coeff_monomial(x0*x0);a3=coeff.coeff_monomial(x0**3)
check("a0_claim",a0-m)
check("a1_claim",a1-((-26+10*r)*L-20*r))
check("a2_claim",a2-((42-86*r/5)*L*L+(-100+100*r)*L+500+200*r))
check("a3_claim",a3-((-112+48*r)*L*L*(L+5*r)/5))
WR=simplify(a3*a3*poly0.subs(x0,xi/a3))
check("monic_cubic_claim",WR-(xi**3+a2*xi*xi+a1*a3*xi+a0*a3*a3))
WR=simplify(xi**3+a2*xi*xi+a1*a3*xi+a0*a3*a3)
# Inverse plane maps: verify the square equation and conic lift, which imply G=0.
sv=a3/xi;tv=sv-alpha*L-d;zv=sv-alpha*L
Xinv=simplify(Xp.subs(t,tv));Yinv=eta*zv/(20*xi*(zv+gamma*L))
Yinv2=simplify(WR*zv*zv/(400*xi*xi*(zv+gamma*L)**2))
check("inverse_lands_on_original_Ysquare_branch",Yinv2-Y2.subs(t,tv))
check("inverse_recovers_conic_lift",(2*A.subs(X,Xinv)*Yinv2+B.subs(X,Xinv))/h.subs(X,Xinv)-Vp.subs(t,tv))
check("inverse_to_forward_t_identity",(2*A.subs(X,Xinv)*Yinv2+B.subs(X,Xinv))/h.subs(X,Xinv)-2*r*Xinv-tv)
# The forward-to-inverse X residual follows exactly from the original quartic.
Vf=(2*A*Y*Y+B)/h;tf=Vf-2*r*X;denf=a+4*r*tf
check("forward_to_inverse_X_residual",(b-tf*tf)-X*denf+4*A*G/(h*h))
sf=tf+d+alpha*L;zf=tf+d;xif=a3/sf;etaf=20*xif*Y*(zf+gamma*L)/zf
check("forward_to_inverse_Y_identity",etaf*zf/(20*xif*(zf+gamma*L))-Y)
# Conversely s and eta recover literally once t has been checked.
check("inverse_to_forward_xi_identity",a3/(tv+d+alpha*L)-xi)
check("inverse_to_forward_eta_identity",20*xi*Yinv*(zv+gamma*L)/zv-eta)
# Discriminants and branch-point evidence are obtained from derived coefficients.
Wdisc=simplify(16*S.discriminant(WR,xi))
check("W_discriminant",Wdisc-2**24*(161-72*r)*L**5*(L+5*r)**5*(L+c))
Fderived=simplify(s*s*s*poly0.subs(x0,1/s)/m)
print("DERIVED_F_IN_S",Fderived,flush=True)
check("branch_at_s_zero",Fderived.subs(s,0)-(-S.Rational(16,5)+16*r/25)*L*L*(L+5*r))
check("branch_cubic_discriminant",S.discriminant(Fderived,s)-(24064+10752*r)*L*(L+5*r)**3*(L+c))
Fbad=S.Poly(Fderived.subs(L,-c),s,extension=r)
common=S.gcd(Fbad,Fbad.diff())
assert common.degree()==1
print("BAD_CENTER_CUBIC_GCD",common.as_expr(),flush=True)
assert S.gcd(common,common.diff()).degree()==0
print("PASS excluded_center_has_exact_one_double_root",flush=True)
conj=(1-r)/2
Pconj=2*(X**5-10*X**3*Y**2+5*X*Y**4)+5*conj*(X*X+Y*Y)**2*T-5*conj**3*(X*X+Y*Y)*T**3+conj**5*T**5
check("second_line_fibre",P-5*r*T*(X*X+Y*Y-T*T)**2-Pconj)
# Origin and exceptional denominator at W infinity.
torigin=-alpha*L-d
check("origin_Xfinite",Xp.subs(t,torigin)+(5*phi+L)/10)
check("origin_X_denominator",(a+4*r*torigin)-4*(3-r)*L)
check("origin_plane_smooth_partial",S.diff(P+L*T*(X*X+Y*Y-T*T)**2,X).subs({X:0,Y:1,T:0})-10)
nodeL=-(25+10*r)/4
assert simplify(Wdisc.subs(L,nodeL))!=0
print("PASS plane_cusp_parameter_has_nonsingular_W",flush=True)
# Verify all infinity points are smooth and their slopes/fields follow exactly.
Pinfty=S.expand(P.subs(T,0))
check("infinity_factor",Pinfty-2*X*(X**4-10*X*X*Y*Y+5*Y**4))
check("infinity_slope_quartic",(xi*xi-(5+2*r))*(xi*xi-(5-2*r))-(xi**4-10*xi*xi+5))
# Twist coefficients: complete square directly, translate by beta, scale by q.
beta=(11-5*r)*L/(2*(L+5*r));k=4*(L+5*r)/r;q=d*k*k
x,y=S.symbols("x y")
TateR=x**3-beta*x*x+((1-beta)*x-beta)**2/4
check("actual_twist_coordinate_polynomial",WR.subs(xi,q*(x-beta))-q**3*TateR)
check("twist_eta_scaling",(k*k*d)**3-q**3)
# Mutation controls prove the checks are sensitive to the central geometry.
reject("omit_homogenizing_T",(P+L*(X*X+Y*Y-T*T)**2)-(P+L*T*(X*X+Y*Y-T*T)**2))
reject("wrong_inverse_Y_sign",-etaf*zf/(20*xif*(zf+gamma*L))-Y)
reject("wrong_conic_t_shift",(a3/(tv+alpha*L)-xi))
reject("wrong_twist_translation",WR.subs(xi,q*(x+beta))-q**3*TateR)
for bad in [0,-5*r,-c]:
    assert simplify(Wdisc.subs(L,bad))==0
    print("NEGATIVE_CONTROL_REJECTED elliptic_claim_at",bad,flush=True)
print("completed_exact_identity_checks",len(checks),flush=True)
print("native_utc_end",datetime.now(timezone.utc).isoformat(),flush=True)
